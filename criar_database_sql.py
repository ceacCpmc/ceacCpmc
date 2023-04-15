from sqlalchemy import Table, create_engine
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import pandas as pd


conn = sqlite3.connect('data.sqlite')
engine = create_engine('sqlite:///data.sqlite')
db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_cpf = db.Column(db.String(11), unique=True, nullable=False)
    user_name = db.Column(db.String(60), nullable=False)
    user_password = db.Column(db.String(60), nullable=False)
    user_email = db.Column(db.String(60), unique=True, nullable=False)
    user_aprovado = db.Column(db.String(1))


User_table = Table('users', Users.metadata)


def create_user_table():
    Users.metadata.create_all(engine)


create_user_table()


c = conn.cursor()
df = pd.read_sql('select * from users', conn)
print(df['user_name'])
print(df['user_cpf'])
print(df['user_password'])
