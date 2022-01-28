from os import environ
import mysql.connector
from .logger import Logger
from .pinger import ping, pinger

logger = Logger()

def get_conn():
    host = environ.get('MYSQL_HOST')
    port=environ.get('MYSQL_PORT')

    # ping database before attempting to connect.
    if ping(host,port) == False: 
        # ping failed.
        if pinger(host,port) == False: return
    try:
        logger.debug("Attempting to connect to database...")
        db = mysql.connector.connect(
               host=host,
               port=port,
               user=environ.get('MYSQL_USER'),
               password=environ.get('MYSQL_PASSWORD'),
               database=environ.get('MYSQL_DATABASE')
               )
        return db
    except:
        logger.error("Failed to connect to database!")
        return False

