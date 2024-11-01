import xml.etree.ElementTree as ET
import psycopg2

from models.connection_model import ConnectionModel

class LoginModel(ConnectionModel):
    def __init__(self):
        super().__init__()
        

    def authenticate(self, username, password):
        connection = self.connect_postgres()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM \"user\" WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        return user is not None
