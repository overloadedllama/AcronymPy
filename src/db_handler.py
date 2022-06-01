import mysql.connector
from mysql.connector.errors import DatabaseError
from configparser import ConfigParser


class DBHandler:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.conn = None
        self.cursor = None

    def init_connection(self):
        parser = ConfigParser()
        parser.read(self.config_file)
        db_info = {}
        if parser.has_section('mysql'):
            params = parser.items('mysql')
            for p in params:
                db_info[p[0]] = p[1]
        else:
            raise Exception('mysql section not found')

        try:
            self.conn = mysql.connector.MySQLConnection(**db_info)
        except Exception:
            raise RuntimeError('Connection Failed')

        self.cursor = self.conn.cursor(buffered=True)

    @staticmethod
    def create_db(config_file='config.ini'):
        parser = ConfigParser()
        parser.read(config_file)

        db_info = {}
        if parser.has_section('mysql'):
            params = parser.items('mysql')
            for p in params:
                if p[0] in {'user', 'password', 'host'}:
                    db_info[p[0]] = p[1]

        conn = mysql.connector.connect(**db_info)
        cursor = conn.cursor()

        sql = "CREATE DATABASE AcronymDB;"

        try:
            cursor.execute(sql)
        except DatabaseError as dbe:
            if dbe.errno == 1007:
                if input('Database "AcronymDB" already exists, do you want to drop it? (y/n) ').lower().startswith('y'):
                    cursor.execute("DROP DATABASE AcronymDB;")
                    cursor.execute(sql)
                else:
                    print('Database not deleted. Exiting from setup...')
                    conn.close()
                    cursor.close()
                    return False

        cursor.execute("USE AcronymDB")

        sql = """create table AcronymRecords (
                    Acronym varchar(20), 
                    FullName varchar(100), 
                    Scope varchar(100),
                    Time datetime,
                    PRIMARY KEY (Acronym, FullName)
                );"""
        cursor.execute(sql)

        cursor.close()
        conn.close()

    def execute_query(self, query, fetch=False):
        self.cursor.execute(query)
        self.conn.commit()
        labels = self.cursor.column_names
        return labels, self.cursor.fetchall() if fetch else None

    def close(self):
        self.conn.close()
        self.cursor.close()
