# AI_Innovation_Hub\logger.py

import logging

def create_logger(logger_name: str = __name__) -> logging.Logger:
    """Creates and configures a logger with INFO level and a console handler."""

    # Obtain a logger instance with the given name
    logger_instance = logging.getLogger(logger_name)
    
    # Set the logging level to INFO
    logger_instance.setLevel(logging.INFO)

    # Check if any handlers are already configured for the logger
    if not logger_instance.handlers:
        # Create a console handler for logging
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Define the log message format
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Apply the formatter to the console handler
        console_handler.setFormatter(log_format)
        
        # Add the console handler to the logger
        logger_instance.addHandler(console_handler)

    return logger_instance