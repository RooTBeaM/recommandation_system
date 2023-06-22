#### use for creating DB local sever

import mysql.connector
from mysql.connector import errorcode
from sqlalchemy import create_engine
import pandas as pd
import os

from config import *
DB_DTT = 'dtt'
DB_AI = 'daytriptour_ai'

# Database setup
def create_database(cursor, DB_NAME):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'UTF8MB4' DEFAULT COLLATE 'UTF8MB4_GENERAL_CI'".format(DB_NAME))

    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

# add dtt and AI schemas
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

try:
    cursor.execute("USE {}".format(DB_DTT))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_DTT))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor, DB_DTT)
        print("Database {} created successfully.".format(DB_DTT))
        cnx.database = DB_DTT
    else:
        print(err)
        exit(1)

try:
    cursor.execute("USE {}".format(DB_AI))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_AI))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor, DB_AI)
        print("Database {} created successfully.".format(DB_AI))
        cnx.database = DB_AI
    else:
        print(err)
        exit(1)

cursor.close()
cnx.close()

# add dtt table to DB_DTT
db_connection_str = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{DB_DTT}"
engine = create_engine(db_connection_str)
ls = os.listdir('../raw_csv/')
for i in ls:
    df = pd.read_csv('../raw_csv/'+i, low_memory=False)
    name = i.split('.')[0]
    df.to_sql(name, con=engine, if_exists='replace', index=False)
    print(name, df.shape)

print('********** Initial Settings Complete **********')