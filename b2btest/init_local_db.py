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
existence_sql = """
    SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
    WHERE SCHEMA_NAME = '{db_name}';
"""
db_creation_sql = """
    CREATE DATABASE {db_name}
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"""
dbs = database_name, f'test_{database_name}'

for db_name in dbs:
    cursor.execute(existence_sql.format(db_name=db_name))
    db_exists = cursor.fetchone()

    if db_exists:
        print(f'Database `{db_name}` exists.')
    else:
        cursor.execute(db_creation_sql.format(db_name=db_name))
        print(f'Database `{db_name}`  created.')


# django user creation
user_exists_sql = f"""
    SELECT COUNT(*) FROM mysql.user
    WHERE user = '{user_name}';
"""
user_create_sql = f"""
    CREATE USER '{user_name}'@'%'
    IDENTIFIED BY '{user_password}';
"""
grant_sql = """
    GRANT ALL PRIVILEGES ON {db_name}.*
    TO '{user_name}'@'%';
"""


cursor.execute(user_exists_sql)
user_exists = cursor.fetchone()[0]

if user_exists:
    print(f'User `{user_name}` already exists.')
else:
    cursor.execute(user_create_sql)
    print(f'User `{user_name}` created.')

for db_name in dbs:
    cursor.execute(
        grant_sql.format(db_name=db_name, user_name=user_name)
    )
    print(f'Privileges `{user_name}`->`{db_name}` granted.')

cursor.execute('FLUSH PRIVILEGES;')
cursor.close()
connection.close()
