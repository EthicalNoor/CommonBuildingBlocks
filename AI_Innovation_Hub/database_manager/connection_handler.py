# AI_Innovation_Hub\database_manager\connection_handler.py

import psycopg2
from contextlib import contextmanager
from ..logger import create_logger
from ...core_sys_config import SystemConfiguration as config
from psycopg2 import sql

logger = create_logger(__name__)

class DBConnectionError(Exception):
    pass

class DatabaseManager:
    """DatabaseManager class encapsulates database-related operations."""
    
    @staticmethod
    def create_database():
        """Ensures that the specified database exists; if not, it creates the database.
        Logs success or failure, including the class and method names."""

        db_params = {
            'dbname': 'postgres',
            'user': config.DB_USER,
            'password': config.DB_PASSWORD,
            'host': config.DB_HOST,
            'port': config.DB_PORT
        }
        
        conn = None
        
        try:
            logger.info(f"Attempting to connect to the 'postgres' database.")
            conn = psycopg2.connect(**db_params)
            conn.autocommit = True
            with conn.cursor() as cursor:
                # Check if the target database already exists
                cursor.execute(
                    sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"),
                    [config.DB_NAME]
                )
                
                if cursor.fetchone():
                    logger.info(f"Database '{config.DB_NAME}' already exists.")
                else:
                    # Create the database if it does not exist
                    cursor.execute(
                        sql.SQL("CREATE DATABASE {}").format(
                            sql.Identifier(config.DB_NAME)
                        )
                    )
                    logger.info(f"Database '{config.DB_NAME}' created successfully.")
                        
        except psycopg2.Error as e:
            logger.error(f"Error creating database: {e}", exc_info=True)
            raise DBConnectionError(f"Failed to create or access the database: {e}") from e
        
        finally:
            if conn:
                conn.close()
                logger.info(f"Database connection closed.")

    @staticmethod
    def create_tables():
        db_params = {
            'dbname': config.DB_NAME,
            'user': config.DB_USER,
            'password': config.DB_PASSWORD,
            'host': config.DB_HOST,
            'port': config.DB_PORT
        }
        conn = None
        try:
            logger.info(f"Attempting to connect to the '{config.DB_NAME}' database.")
            conn = psycopg2.connect(**db_params)
            conn.autocommit = True
            with conn.cursor() as cursor:
                schema = config.TABLE_SCHEMA
                
                logger.info(f"Using schema: {schema}")
                
                # Construct column definitions and primary key constraint
                columns = ", ".join(
                    [f"{col_name} {col_type}" for col_name, col_type in schema.items() if col_name != "PRIMARY_KEY"]
                )
                primary_key = f"CONSTRAINT pk_your_table_name_here PRIMARY KEY ({schema['PRIMARY_KEY']})"
                
                create_table_query = f"""
                CREATE TABLE IF NOT EXISTS your_table_name_here (
                    {columns},
                    {primary_key}
                );
                """
                
                cursor.execute(create_table_query)
                logger.info(f"Table 'your_table_name_here' created or already exists.")
                    
        except psycopg2.Error as e:
            logger.error(f"Error creating table: {e}", exc_info=True)
            raise DBConnectionError(f"Failed to create or access the table: {e}") from e
        finally:
            if conn:
                conn.close()  # Ensure connection is properly closed
                logger.info(f"Database connection closed.")

@contextmanager
def get_db_connection():
    conn = None
    try:
        logger.info(f"Attempting to connect to the '{config.DB_NAME}' database.")
        conn = psycopg2.connect(
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT
        )
        logger.info(f"Connection established to database '{config.DB_NAME}'.")
        yield conn
    
    except psycopg2.OperationalError as e:
        logger.error(f"Failed to establish database connection: {e}", exc_info=True)
        raise DBConnectionError("Failed to connect to the database.") from e
    finally:
        if conn:
            conn.close()
            logger.info(f"Database connection closed.")