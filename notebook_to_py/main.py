import pandas as pd
import os

from common import *
from preprocess import *
from vector import *

order_col = [
    'customer_id','order_product_id','browser', 'platform',
    'customer_firstname','customer_lastname','customer_email','customer_gender', 
    'customer_nationality','customer_country','customer_phone_iso','customer_phone_code', 
    'order_price_paid','order_state','order_payment_by',
    'order_quantity_infant','order_quantity_children','order_quantity_adult','order_quantity_elder', 
    'order_departure_date','date_create',
    ]
full_cols = [
    'new_id', 'product_id', 'browser', 'platform', 'customer_gender','country_code',
    'booked_days', 'order_price_paid', 
    'sum_kids', 'sum_adults',
    'private', 'group', 'family',
    'cat_1', 'cat_2', 'cat_3', 'cat_4', 'cat_5', 'cat_6', 'cat_7', 'cat_8', 'cat_9', 
    'cat_10', 'cat_11', 'cat_12', 'cat_13', 'cat_14', 'cat_15', 'cat_16','cat_17', 'cat_18' 
    ]
vector_cols = [
    # 'new_id', 'order_product_id', 'browser', 'platform', 'customer_gender','country_code', # groupby mean
    'booked_days', 'order_price_paid', 
    'sum_kids', 'sum_adults',
    'private', 'group', 'family',
    'cat_1', 'cat_2', 'cat_3', 'cat_4', 'cat_5', 'cat_6', 'cat_7', 'cat_8', 'cat_9',
    'cat_10', 'cat_11', 'cat_12', 'cat_13', 'cat_14', 'cat_15', 'cat_16','cat_17', 'cat_18'
    ]

cat_cols = [
    'cat_1', 'cat_2', 'cat_3', 'cat_4', 'cat_5', 'cat_6', 'cat_7', 'cat_8', 'cat_9',
    'cat_10', 'cat_11', 'cat_12', 'cat_13', 'cat_14', 'cat_15', 'cat_16','cat_17', 'cat_18'
    ]
test_productID = [
    22, 23, 24, 25, 26, 27, 28, 
    30, 31, 32, 36, 37, 
    40, 41, 45, 48, 53, 59,
    61, 62, 63, 66,
    71, 72, 74, 77,
    85, 86, 89, 93, 94, 95, 96, 99,
    100, 101, 104, 106, 107, 108,
    110, 112, 114, 116,
    126, 168, 201]

# load data
df_user = pd.read_csv('../raw_csv/dtt_users.csv')
df_country = pd.read_csv('../raw_csv/dtt_country.csv')[['country_id','country_code','country_phonecode','country_name']]
df_order = pd.read_csv('../raw_csv/dtt_order.csv')[order_col]
df_product_cat = pd.read_csv('../raw_csv/dtt_product_category.csv')

df_product = pd.read_csv('../raw_csv/dtt_product.csv')
df_product = df_product[~df_product['product_id'].isin(test_productID)]

# URLs
productID_to_url = {i[1][0] : 'www.daytriptour.com/trip/' + i[1][1] for i in df_product.iterrows()}

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

# CLEAN_DIR = './clean_data/'
# save_csv(df_order, CLEAN_DIR, subname='')

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

# MERGE_DIR = './merge_data/'
# df_order_v1 = pd.read_csv(select_csv_path(MERGE_DIR))
# CheckProductID(df_product,df_order_v1)
# save_csv(df_order_v1, MERGE_DIR, subname='')

# # Create Vectors
VECTOR_DIR = './vector_data/'
# try:
#     df_full_vector = pd.read_csv(select_csv_path(MERGE_DIR))[full_cols]

#     # intial values for zero in Category columns
#     c = 0.0
#     df_full_vector = EncodeVector(df_full_vector, cat_cols, c)
#     CreateVector(df_full_vector, vector_cols, VECTOR_DIR)
#     print('Creating Vectors is completed')
# except:
#     print('Creating Vectors was Failed')
#     os._exit(0) 

# # Create Matrixs
MATRIX_DIR = './matrix_data/'

# try:
df_user_vector = pd.read_csv(select_csv_path(VECTOR_DIR+'user/'))
df_product_vector = pd.read_csv(select_csv_path(VECTOR_DIR+'product/'))

similarity_cols = [
    # 'booked_days', 
    'order_price_paid', 
    'sum_kids','sum_adults', 
    # 'private', 'group', 'family', 
    'cat_1', 'cat_2', 'cat_3','cat_4', 'cat_5', 'cat_6', 'cat_7', 'cat_8', 'cat_9', 'cat_10',
    'cat_11', 'cat_12', 'cat_13', 'cat_14', 'cat_15', 'cat_16', 'cat_17','cat_18'
    ]
df_user_item_similarity = compute_similarity(df_user_vector, df_product_vector, 'new_id', 'product_id', similarity_cols)
save_csv(df_user_item_similarity, MATRIX_DIR, subname='user_item', idx = True)

df_item_item_similarity = compute_similarity(df_product_vector, df_product_vector, 'product_id', 'product_id', similarity_cols)
save_csv(df_item_item_similarity, MATRIX_DIR, subname='item_item', idx = True)

df_user_user_similarity = compute_similarity(df_user_vector, df_user_vector, 'new_id', 'new_id', similarity_cols)
save_csv(df_user_user_similarity, MATRIX_DIR, subname='user_user', idx = True)




