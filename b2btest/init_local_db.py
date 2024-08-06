"""
This module is meant to be used only once during the local
deployment step. It includes checks for the existence
of user and database. However, please avoid using it
if you have a database with valuable data, as the module
has not yet been covered by tests.
"""

import os

import MySQLdb


root_password = os.getenv('MYSQL_ROOT_PASSWORD')
database_host = os.getenv('DB_HOST')
database_name = os.getenv('DB_NAME')
user_name = os.getenv('DB_USER')
user_password = os.getenv('DB_PASSWORD')


connection = MySQLdb.connect(
    host=database_host,
    user='root',
    passwd=root_password
)

cursor = connection.cursor()

# django db creation
cursor.execute(
    f"""
    SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
    WHERE SCHEMA_NAME = '{database_name}';
    """
)
db_exists = cursor.fetchone()

if db_exists:
    print('Database exists.')
else:
    cursor.execute(
        f"""
        CREATE DATABASE IF NOT EXISTS {database_name}
        CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        """
    )
    print('Database created.')

# django user creation
cursor.execute(
    f"""
    SELECT COUNT(*) FROM mysql.user
    WHERE user = '{user_name}';
    """
)
user_exists = cursor.fetchone()[0]

if user_exists:
    print('User already exists.')
else:
    cursor.execute(
        f"""
        CREATE USER '{user_name}'@'%'
        IDENTIFIED BY '{user_password}';
        """
    )
    cursor.execute(
        f"""
        GRANT ALL PRIVILEGES ON {database_name}.*
        TO '{user_name}'@'%';
        """
    )
    cursor.execute('FLUSH PRIVILEGES;')
    print('User created and privileges granted.')

cursor.close()
connection.close()
