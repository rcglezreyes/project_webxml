import xml.etree.ElementTree as ET
import psycopg2
import socket
import uuid

class ConnectionModel:
    
    def __init__(self):
        self.config = self.load_config()
        self.conn = self.connect_postgres()

    def load_config(self):
        tree = ET.parse("config/connection.xml")
        root = tree.getroot()

        config = {
            "host": root.find("./database/host").text,
            "port": root.find("./database/port").text,
            "dbname": root.find("./database/dbname").text,
            "user": root.find("./database/user").text,
            "password": root.find("./database/password").text
        }
        return config

    def connect_postgres(self):
        conn = psycopg2.connect(
            host=self.config["host"],
            port=self.config["port"],
            dbname=self.config["dbname"],
            user=self.config["user"],
            password=self.config["password"]
        )
        # print("Successfully connected to Database in PostgreSQL")
        return conn

    def close_connection(self):
        self.conn.close()
        # print("Connection closed")
        
    def select_user(self, username):
        query = "SELECT * FROM \"user\" WHERE username = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()
        return user
    
    def get_ip(self):
        hostname = socket.gethostname()  
        ip_address = socket.gethostbyname(hostname)  
        return ip_address
    
    def get_mac(self):
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 8)][::-1])
        return mac_address