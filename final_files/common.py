from pathlib import Path
from datetime import datetime
from glob import glob
from sqlalchemy import create_engine
import pandas as pd
import os

from config import *

def save_csv(df, dir, subname='', idx=False):
    time = datetime.now().strftime('%Y%m%d_%H%M')
    full_dir = os.path.join('.',dir,subname)
    Path(full_dir).mkdir(parents=True, exist_ok=True)
    full_path = os.path.join('.',dir,subname,f'{time}.csv')
    df.to_csv(full_path, index=idx)
    print(f'saved: {full_path}')

def select_csv_path(dir):
    pth = os.path.join('.',dir,'*.csv')
    dirFiles = [Path(x).name for x in glob(pth)]
    if dirFiles !=[]:
        dirFiles.sort(reverse=True)
        filePath = os.path.join('.',dir,dirFiles[0])
        print(f'read: {filePath}')
    else:
        print('CSV File was not found')
    return Path(filePath)

def CheckProductID(df_order_v1):
    df_product = query_dtt('dtt_product')
    df_product = df_product[~df_product['product_id'].isin(test_productID)]
    product_ids_not_present = ~df_product['product_id'].isin(df_order_v1['product_id'])
    product_ids_list = df_product.loc[product_ids_not_present, 'product_id'].tolist()
    print("Product IDs not present in df_product_matrix:" , len(product_ids_list))
    print(product_ids_list)

def print_product_links(product_ls, productID_to_url):
    # print("Product Links:")
    for product_id in product_ls:
        print(productID_to_url[product_id])

def query_dtt(table):
    db_connection_str = f"mysql+pymysql://{config_dtt['user']}:{config_dtt['password']}@{config_dtt['host']}:{config_dtt['port']}/{config_dtt['database']}"
    engine = create_engine(db_connection_str)
    df = pd.read_sql(f'SELECT * FROM dtt.{table}', con=engine)
    print(f'READ DB_DTT: {table}')
    return df

def query_AI(table, subname='', log=False):
    db_connection_str = f"mysql+pymysql://{config_ai['user']}:{config_ai['password']}@{config_ai['host']}:{config_ai['port']}/{config_ai['database']}"
    engine = create_engine(db_connection_str)
    if subname:
        fullname = table+'_'+subname
    else:
        fullname = table
    df = pd.read_sql(f'SELECT * FROM daytriptour_ai.{fullname}', con=engine)
    if log: 
        print(f'READ DB_AI: {fullname}')
    return df

def update_AI(df, table, subname='', idx=False):
    db_connection_str = f"mysql+pymysql://{config_ai['user']}:{config_ai['password']}@{config_ai['host']}:{config_ai['port']}/{config_ai['database']}"
    engine = create_engine(db_connection_str)
    if subname:
        fullname = table+'_'+subname
    else:
        fullname = table
    df.to_sql(fullname, con=engine, if_exists='replace', index=idx)
    # print(f'UPDATE DB: {fullname} is completed')
