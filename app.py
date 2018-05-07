import os

from flask import Flask
from peewee import PostgresqlDatabase, SqliteDatabase
from micawber import bootstrap_basic

SECRET_KEY = 'you-will-never-guess-my-secret-key'
APP_ROOT = os.path.dirname(os.path.realpath(__file__))

UPLOAD_FOLDER = 'static/img/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config.from_object(__name__)

pg_db = PostgresqlDatabase('db',
                           user='user',
                           password='password',
                           host='localhost',
                           port=6432)

oembed = bootstrap_basic()

# pg_db = SqliteDatabase('test.db')

# docker run -p 6432:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=db -v /home/yuriy/postgres_db/:/var/lib/postgresql/data -d postgres:9.6
