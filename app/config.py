# PostgreSQL
# DATABASE = {
#     'dialect': 'postgresql',
#     'driver': 'psycopg2',
#     'username': 'postgres',
#     'password': 'GiggaNigg4$',
#     'host': 'localhost',
#     'port': '5432',
#     'database': 'imads'
# }

# DATABASE_URL = (  
#     f"{DATABASE['dialect']}+{DATABASE['driver']}://"  
#     f"{DATABASE['username']}:{DATABASE['password']}@"  
#     f"{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}"  
# )


# SQLite
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'imads')
    APP_NAME = os.environ.get('APP_NAME', 'imads')


    SQLALCHEMY_DATABASE_URI = 'sqlite:///imads.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False