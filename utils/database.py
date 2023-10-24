import time
import datetime as dt
import mysql.connector

from utils.logger import info_log, error_log

class SuggestionDatabase:

    def __init__(self, db: mysql.connector.MySQLConnection):

        self.__db = db
        self.__cursor = self.__db.cursor()

        self.__cursor.execute('SHOW DATABASES')
        databases_list = [db[0] for db in self.__cursor.fetchall()]

        if 'celestial_suggestions' not in databases_list:
            error_log('Error: Suggestions database not found.')
            info_log('Creating suggestions database...')
            self.__create_database()
            info_log('Suggestion database created successfully.')

        self.__cursor.execute(f'USE celestial_suggestions')


    def __create_database(self) -> None:

        self.__cursor.execute('CREATE DATABASE celestial_suggestions')

        self.__cursor.execute('USE celestial_suggestions')
        self.__cursor.execute('SET time_zone = "+07:00"')

        self.__cursor.execute(
            """
                CREATE TABLE legacy_suggestions (
                    user VARCHAR(255) NOT NULL, 
                    bot_input VARCHAR(4000) NOT NULL, 
                    responses VARCHAR(4000) NOT NULL, 
                    notes VARCHAR(4000), 
                    timestamp TIMESTAMP
                )
            """
        )
        
        self.__cursor.execute(
            """
                CREATE TABLE dl_suggestions (
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
        
        self.__cursor.execute(query, data)
        self.__db.commit()


def create_database_connection(host: str, user: str, password: str) -> mysql.connector.MySQLConnection:

    '''
        Connect to mysql database with the given credential.
    '''

    info_log('Connecting to database...')

    db = mysql.connector.connect(
        host = host,
        user = user,
        password = password
    )

    info_log('Connected to database.')
    return db