# AI_Innovation_Hub\queue_dispatcher\mq_handler.py

import pika
import json
import ssl
from pika import SSLOptions, exceptions as pika_exceptions
from ..logger import create_logger

logger = create_logger(__name__)

class MQConnectionError(Exception):
    """Custom exception for RabbitMQ connection errors."""
    pass

class MessageProcessingError(Exception):
    """Custom exception for errors occurring during message processing."""
    pass

class SSLConfigurationError(Exception):
    """Custom exception for SSL configuration errors."""
    pass

class RabbitMQHandler:
    """Class to handle RabbitMQ connections and message processing."""

    def __init__(self, host: str, port: int, user: str, password: str):
        self.host = host
        self.port = port
        self.credentials = pika.PlainCredentials(user, password)
        self.ssl_options = self._configure_ssl_options(host)

    def _configure_ssl_options(self, mq_host: str) -> SSLOptions:
        """Set up SSL options for secure communication with RabbitMQ."""
        try:
            context = ssl.create_default_context()
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = True
            
            return SSLOptions(context, mq_host)
        except Exception as error:
            logger.error(f"Error setting up SSL options: {error}", exc_info=True)
            raise SSLConfigurationError("Failed to set up SSL for RabbitMQ.")

    def _handle_message(self, channel, method, properties, body, callback):
        """Process incoming messages from the RabbitMQ queue."""
        try:
            message = json.loads(body)
            logger.info(f"Received message: {message}")
            callback(channel, method, properties, message)
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON message.", exc_info=True)
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as error:
            logger.error(f"An error occurred while processing the message: {error}", exc_info=True)
            raise MessageProcessingError(f"Error processing message: {error}")

    def start_listener(self, exchange_name: str, queue_name: str, callback) -> None:
        """Set up the RabbitMQ listener and start consuming messages."""
        connection_parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=self.credentials,
            ssl_options=self.ssl_options,
            connection_attempts=5,
            retry_delay=5,
            heartbeat=600,
            blocked_connection_timeout=300
        )
        
        try:
            connection = pika.BlockingConnection(parameters=connection_parameters)
            channel = connection.channel()
            
            channel.exchange_declare(exchange=exchange_name, exchange_type="fanout", durable=True)
            channel.queue_declare(queue=queue_name, durable=True)
            channel.queue_bind(queue=queue_name, exchange=exchange_name)
            
            channel.basic_consume(
                queue=queue_name,
                on_message_callback=lambda ch, method, props, body: self._handle_message(ch, method, props, body, callback),
                auto_ack=False
            )
            
            logger.info(f"Listening to queue '{queue_name}'")
            channel.start_consuming()
        except pika_exceptions.AMQPChannelError as error:
            logger.error(f"Channel error occurred: {error}", exc_info=True)
            raise
        except Exception as error:
            logger.error(f"Failed to set up RabbitMQ listener: {error}", exc_info=True)
            raise MQConnectionError("Failed to set up RabbitMQ listener.") from error
