import mysql.connector

def db_connector():
    db = mysql.connector.connect(
        host = "127.0.0.1",
        user = "root",
        password = "root",
        database = "db"
    )
    
    return db

