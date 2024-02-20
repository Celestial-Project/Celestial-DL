import time
import datetime as dt
import mysql.connector

from utils.logger import info_log, error_log

class SuggestionDatabase:

    def __init__(self, db: mysql.connector.MySQLConnection):

        self.__db = db
        self.__cursor = self.__db.cursor()

        self.__initialize_database()
        
        
    def __execute_query(self, query: str):

        self.__db.ping(reconnect = True)
        result = self.__cursor.execute(query)
        
        return result
    
    
    def __execute_query_with_data(self, query: str, data: dict):

        self.__db.ping(reconnect = True)
        
        result = self.__cursor.execute(query, data)
        self.__db.commit()
        
        return result
    
    
    def __initialize_database(self) -> None:
        
        info_log('Initializing database...')
        
        self.__execute_query('CREATE DATABASE IF NOT EXISTS celestial_suggestions')
        
        self.__execute_query('USE celestial_suggestions')
        self.__execute_query('SET time_zone = "+07:00"')

        self.__execute_query(
            """
                CREATE TABLE IF NOT EXISTS legacy_suggestions (
                    user VARCHAR(255) NOT NULL, 
                    bot_input VARCHAR(4000) NOT NULL, 
                    responses VARCHAR(4000) NOT NULL, 
                    notes VARCHAR(4000), 
                    timestamp TIMESTAMP
                )
            """
        )
        
        self.__execute_query(
            """
                CREATE TABLE IF NOT EXISTS dl_suggestions (
                    user VARCHAR(255) NOT NULL, 
                    bot_input VARCHAR(4000) NOT NULL, 
                    responses VARCHAR(4000) NOT NULL, 
                    notes VARCHAR(4000), 
                    timestamp TIMESTAMP
                )
            """
        )


    def add_suggestion(self, table_name: str, user: str, bot_input: str, responses: str, notes: str = '') -> None:

        time_epoch = time.time()
        timestamp = dt.datetime.fromtimestamp(time_epoch).strftime('%Y-%m-%d %H:%M:%S')

        data = {
            'user': user,
            'bot_input': bot_input,
            'responses': responses,
            'notes': notes,
            'timestamp': timestamp
        }

        query = f"""
            INSERT INTO {table_name} (
                user, 
                bot_input, 
                responses, 
                notes, 
                timestamp
            )
             
            VALUES (
                %(user)s, 
                %(bot_input)s, 
                %(responses)s, 
                %(notes)s, 
                %(timestamp)s
            )
        """
        
        self.__execute_query_with_data(query, data)
    

def create_database_connection(host: str, user: str, password: str) -> mysql.connector.MySQLConnection:

    '''
        Connect to mysql database with the given credential.
    '''

    info_log('Connecting to database...')

    try:
        db = mysql.connector.connect(
            host = host,
            user = user,
            password = password
        )
        
    except mysql.connector.Error:
        error_log('Error: cannot create database connection to MySQL database.')
        exit(1)

    info_log('Connected to database.')
    return db