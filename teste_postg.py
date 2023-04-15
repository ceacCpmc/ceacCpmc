import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import Table, create_engine
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
import sqlite3


# conn = psycopg2.connect(host='ec2-3-217-14-181.compute-1.amazonaws.com', database='d1ebsibpj32fe7',
# user='dtljqrsrjbmfto', password='f26f79c64700fad73a8b6c088ee579b711ffa82ebc88ae9cf80724939548d4bd')
#
#
# engine = create_engine('postgresql://dtljqrsrjbmfto:f26f79c64700fad73a8b6c088ee579b711ffa82ebc88ae9cf80724939548d4bd@ec2'
#                        '-3-217-14-181.compute-1.amazonaws.com:5432/d1ebsibpj32fe7')

conn = psycopg2.connect(host='ec2-3-210-173-88.compute-1.amazonaws.com', database='d15949k84tt69d',
                        user='evgdmltwwnjdfn',
                        password='f3623d6aae90a95d478cc153c816846d9d615c3ca60385e536f76e56a175dca0')

engine = create_engine(
    'postgresql://evgdmltwwnjdfn:f3623d6aae90a95d478cc153c816846d9d615c3ca60385e536f76e56a175dca0@ec2' \
      '-3-210-173-88.compute-1.amazonaws.com:5432/d15949k84tt69d')



db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_cpf = db.Column(db.String(11), unique=True, nullable=False)
    user_name = db.Column(db.String(60), nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(60), unique=True, nullable=False)
    user_aprovado = db.Column(db.String(1))


User_table = Table('users', Users.metadata)


def create_user_table():
    Users.metadata.create_all(engine)


create_user_table()


c = conn.cursor()
df = pd.read_sql('select * from users', conn)
print(df)
conn.close()
#####################################################################################################



