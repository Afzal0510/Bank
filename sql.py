import mysql.connector
from mysql.connector import errorcode

config = {
    'user': 'root',
    'password': 'Afzal0510',
    'port': '3306',
}

try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    print("Connected to MySQL server")

    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS banks")
        print("Database 'banks' created")
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")
        exit()

    cursor.execute("USE banks")

    create_users_table = ("""
    CREATE TABLE IF NOT EXISTS users (
        username VARCHAR(30) PRIMARY KEY,
        password VARCHAR(18),
        balance FLOAT DEFAULT 0.00
    )
    """)
    cursor.execute(create_users_table)
    print("Table 'users' created")

    create_history_log_table = ("""
    CREATE TABLE IF NOT EXISTS history_log (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(30),
        history_description VARCHAR(190),
        history_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (username) REFERENCES users(username)
    )
    """)
    cursor.execute(create_history_log_table)
    print("Table 'history_log' created")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if 'cnx' in locals() and cnx.is_connected():
        cursor.close()
        cnx.close()
        print("MySQL connection closed")
