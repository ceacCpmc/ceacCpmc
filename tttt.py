@profile
def my_func():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b, a
    # return a

if __name__ == '__main__':
    my_func()

import pandas as pd
from sqlalchemy import Table, create_engine
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import  generate_password_hash, check_password_hash
import sqlite3
import warnings

conn = sqlite3.connect('data.sqlite')
engine = create_engine('sqlite:///data.sqlite')
c = conn.cursor()
df = pd.read_sql('select * from users', conn)
df
conn.close()








