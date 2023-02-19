import mysql.connector


class UseDatabase:

    def __init__(self, config: dict) -> None:
        """initializes all of the class state or attributes"""
        
        self.configuration = config

    def __enter__(self) -> 'cursor':
        """The dunder enter setup our connection with the mysql database and returns a  cursor object"""
        
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        """The dunder exit teardown our connection with the mysql database"""
        
        self.conn.commit()
        self.cursor.close()
        self.conn.close()