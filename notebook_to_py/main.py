import pandas as pd
import os

from common import *
from preprocess import *

order_col = [
    'customer_id','order_product_id','browser', 'platform',
    'customer_firstname','customer_lastname','customer_email','customer_gender', 
    'customer_nationality','customer_country','customer_phone_iso','customer_phone_code', 
    'order_price_paid','order_state','order_payment_by',
    'order_quantity_infant','order_quantity_children','order_quantity_adult','order_quantity_elder', 
    'order_departure_date','date_create',
    ]
vector_cols = [
    'new_id', 'product_id', 'browser', 'platform', 'customer_gender','country_code',
    'booked_days', 'order_price_paid', 
    'sum_kids', 'sum_adults',
    'private', 'group', 'family',
    'cat_1', 'cat_2', 'cat_3', 'cat_4', 'cat_5', 'cat_6', 'cat_7', 'cat_8', 'cat_9', 
    'cat_10', 'cat_11', 'cat_12', 'cat_13', 'cat_14', 'cat_15', 'cat_16','cat_17', 'cat_18' 
    ]
cat_cols = ['cat_1', 'cat_2', 'cat_3', 'cat_4', 'cat_5', 'cat_6', 'cat_7', 'cat_8', 'cat_9',
    'cat_10', 'cat_11', 'cat_12', 'cat_13', 'cat_14', 'cat_15', 'cat_16','cat_17', 'cat_18']

# load data
df_user = pd.read_csv('../raw_csv/dtt_users.csv')
df_country = pd.read_csv('../raw_csv/dtt_country.csv')[['country_id','country_code','country_phonecode','country_name']]
df_order = pd.read_csv('../raw_csv/dtt_order.csv')[order_col]
df_product_cat = pd.read_csv('../raw_csv/dtt_product_category.csv')


print('-'*15, 'Data Loaded', '-'*15)
print(f'Total orders : {len(df_order)}')

# # Drop NAN
# try:
#     df_order = CleanDrop(df_order)
#     print('Cleaning Data is completed')
# except:
#     print('Drop NAN in Cleaning Process was Failed')
#     os._exit(0)

# # Encode
# try:
#     df_order = CleanEncode(df_order, df_country)
#     print('Encoding Data for Orders is completed')
#     print(f'Dataframe shape : {df_order.shape}')
#     print(f'Dataframe columns name : \n{df_order.columns}\n')
# except:
#     print('Encoding in Cleaning Process was Failed')
#     os._exit(0)

# FOLDER_CLEAN_DIR = './clean_data/'
# save_csv(df_order, FOLDER_CLEAN_DIR, name='')

# # Product category
# try:
#     df_product_cat = ProductEncode(df_product_cat)
#     print(f'Total products : {len(df_product_cat)}')
#     print('Encoding Data for Products is completed')
#     print(f'Dataframe shape : {df_product_cat.shape}')
#     print(f'Dataframe columns name : \n{df_product_cat.columns}\n')
# except:
#     print("Encoding Product's Categories was Failed")
#     os._exit(0)    

# # Mearge product category
# try:
#     df_order_v1 = pd.merge(df_order[df_order['order_state']==2], df_product_cat, on='product_id')
#     print('Merging Product catagory is completed')
#     print(f'Dataframe shape : {df_order_v1.shape}')
#     print(f'Dataframe columns name : \n{df_order_v1.columns}\n')
# except:
#     print("Mearging Product's Categories was Failed")
#     os._exit(0)    

# # New User ID
# start_newID = 10000
# use_cols = [
#     'customer_id', 'new_id', 'product_id', 'browser', 'platform',
#     'customer_firstname', 'customer_lastname', 'customer_email',
#     'customer_gender', 'customer_nationality', 'customer_country',
#     'customer_phone_iso', 'customer_phone_code', 'order_price_paid',
#     'order_state', 'order_payment_by', 'order_quantity_infant',
#     'order_quantity_children', 'order_quantity_adult',
#     'order_quantity_elder', 'order_departure_date', 'date_create',
#     'booked_days', 'departure_year', 'departure_month', 'departure_day',
#     'departure_DayofYear', 'departure_DayofWeek', 'country_code',
#     'sum_kids', 'sum_adults', 'private', 'group', 'family', 'cat_1',
#     'cat_2', 'cat_3', 'cat_4', 'cat_5', 'cat_6', 'cat_7', 'cat_8', 'cat_9',
#     'cat_10', 'cat_11', 'cat_12', 'cat_13', 'cat_14', 'cat_15', 'cat_16',
#     'cat_17', 'cat_18']

# try:
#     df_order_v1, end_newID = CreateNewID(df_order_v1, start_newID, use_cols)
#     print('Creating New UserID is completed')
#     print(f'New UserID start from {start_newID} to {end_newID}')
# except:
#     print('Creating New UserID was Failed')
#     os._exit(0)    

FOLDER_MERGE_DIR = './merge_data/'
# save_csv(df_order_v1, FOLDER_MERGE_DIR, name='')

# Create Vectors
df_full_matrix = pd.read_csv(select_csv_path(FOLDER_MERGE_DIR))[vector_cols]
print(df_full_matrix.head())




