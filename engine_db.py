from sqlalchemy import create_engine

# Подключение к серверу PostgreSQL на localhost с помощью psycopg2 DBAPI 
engine = create_engine("sqlite:///D:\\WORKWORK\\DND\\dnd-game-backend\\dnd-game")

engine.connect()

engine.begin()

# import psycopg2
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# # Устанавливаем соединение с postgres
# connection = psycopg2.connect(user="postgres", password="1111")
# connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# # Создаем курсор для выполнения операций с базой данных
# cursor = connection.cursor()
# # sql_create_database = 
# # Создаем базу данных
# cursor.execute('create database DND')
# # Закрываем соединение
# cursor.close()
# connection.close()

# import psycopg2
# from psycopg2 import sql
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE

# con = psycopg2.connect(dbname='dnd',
#       user="postgres", host='localhost', port='5432',
#       password='postgres')

# con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE

# cur = con.cursor()

# # Use the psycopg2.sql module instead of string concatenation 
# # in order to avoid sql injection attacks.
# cur.execute(sql.SQL("CREATE DATABASE {}").format(
#         sql.Identifier('dnd_game'))
#     )
