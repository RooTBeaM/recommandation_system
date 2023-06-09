import mysql.connector
from mysql.connector import errorcode
from sqlalchemy import create_engine
import pandas as pd
import os

from config import *
from common import *
from preprocess import *
from vector import *
from update_product import *

DB_DTT = 'dtt'
DB_AI = 'AI'

# directory
CLEAN_DIR = 'clean_data'
VECTOR_DIR = 'vector_data'
MERGE_DIR = 'merge_data'
MATRIX_DIR = 'matrix_data'


order_col = [
    'customer_id','order_product_id','browser', 'platform',
    'customer_firstname','customer_lastname','customer_email','customer_gender', 
    'customer_nationality','customer_country','customer_phone_iso','customer_phone_code', 
    'order_price_paid','order_state','order_payment_by',
    'order_quantity_infant','order_quantity_children','order_quantity_adult','order_quantity_elder', 
    'order_departure_date','date_create']
use_cols = [
    'customer_id', 'new_id', 'product_id', 'browser', 'platform',
    'customer_firstname', 'customer_lastname', 'customer_email',
    'customer_gender', 'customer_nationality', 'customer_country',
    'customer_phone_iso', 'customer_phone_code', 'order_price_paid',
    'order_state', 'order_payment_by', 'order_quantity_infant',
    'order_quantity_children', 'order_quantity_adult',
    'order_quantity_elder', 'order_departure_date', 'date_create',
    'booked_days', 'departure_year', 'departure_month', 'departure_day',
    'departure_DayofYear', 'departure_DayofWeek', 'country_code',
    'sum_kids', 'sum_adults', 'private', 'group', 'family', 'cat_1',
    'cat_2', 'cat_3', 'cat_4', 'cat_5', 'cat_6', 'cat_7', 'cat_8', 'cat_9',
    'cat_10', 'cat_11', 'cat_12', 'cat_13', 'cat_14', 'cat_15', 'cat_16',
    'cat_17', 'cat_18']
full_cols = [
    'new_id', 'product_id', 'browser', 'platform', 'customer_gender','country_code',
    'booked_days', 'order_price_paid', 
    'sum_kids', 'sum_adults',
    'private', 'group', 'family',
    'cat_1', 'cat_2', 'cat_3', 'cat_4', 'cat_5', 'cat_6', 'cat_7', 'cat_8', 'cat_9', 
    'cat_10', 'cat_11', 'cat_12', 'cat_13', 'cat_14', 'cat_15', 'cat_16','cat_17', 'cat_18' ]
vector_cols = [
    # 'new_id', 'order_product_id', 'browser', 'platform', 'customer_gender','country_code', # groupby mean
    'booked_days', 'order_price_paid', 
    'sum_kids', 'sum_adults',
    'private', 'group', 'family',
    'cat_1', 'cat_2', 'cat_3', 'cat_4', 'cat_5', 'cat_6', 'cat_7', 'cat_8', 'cat_9',
    'cat_10', 'cat_11', 'cat_12', 'cat_13', 'cat_14', 'cat_15', 'cat_16','cat_17', 'cat_18']
similarity_cols = [
    # 'booked_days', 
    'order_price_paid', 
    'sum_kids','sum_adults', 
    # 'private', 'group', 'family', 
    'cat_1', 'cat_2', 'cat_3','cat_4', 'cat_5', 'cat_6', 'cat_7', 'cat_8', 'cat_9', 'cat_10',
    'cat_11', 'cat_12', 'cat_13', 'cat_14', 'cat_15', 'cat_16', 'cat_17','cat_18']
distance_cols = [
    'booked_days', 
    'order_price_paid', 
    'sum_kids','sum_adults', 
    'private', 'group', 'family', 
    'cat_1', 'cat_2', 'cat_3','cat_4', 'cat_5', 'cat_6', 'cat_7', 'cat_8', 'cat_9', 'cat_10',
    'cat_11', 'cat_12', 'cat_13', 'cat_14', 'cat_15', 'cat_16', 'cat_17','cat_18']
cat_cols = [
    'cat_1', 'cat_2', 'cat_3', 'cat_4', 'cat_5', 'cat_6', 'cat_7', 'cat_8', 'cat_9',
    'cat_10', 'cat_11', 'cat_12', 'cat_13', 'cat_14', 'cat_15', 'cat_16','cat_17', 'cat_18']
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

df_product = query_dtt('dtt_product')
df_product = df_product[~df_product['product_id'].isin(test_productID)]

# URLs
productID_to_url = {i[1][0] : 'www.daytriptour.com/trip/' + i[1][2] for i in df_product.iterrows()}

def mode_0():
    # load data
    df_user = query_dtt('dtt_users')
    df_country = query_dtt('dtt_country')[['country_id','country_code','country_phonecode','country_name']]
    df_order = query_dtt('dtt_order')[order_col]
    df_product_cat = query_dtt('dtt_product_category')
    print('-'*15, 'Data Loaded', '-'*15)
    print(f'Total orders : {len(df_order)}')

    # Drop NAN
    try:
        df_order = CleanDrop(df_order)
        print('Cleaning Data is completed')
    except:
        print('Drop NAN in Cleaning Process was Failed')
        os._exit(0)

    # Encode
    try:
        df_order = CleanEncode(df_order, df_country)
        print(f'Dataframe shape : {df_order.shape}')
        print(f'Dataframe columns name : \n{df_order.columns}\n')
        print('Encoding Data for Orders is completed')
        print('-'*50,'\n')
    except:
        print('Encoding in Cleaning Process was Failed')
        os._exit(0)

    # save_csv(df_order, CLEAN_DIR, subname='')
    update_AI(df_order, CLEAN_DIR)

    # Product category
    try:
        df_product_cat = ProductEncode(df_product_cat)
        print(f'Total products : {len(df_product_cat)}')
        print(f'Dataframe shape : {df_product_cat.shape}')
        print(f'Dataframe columns name : \n{df_product_cat.columns}\n')
        print('Encoding Data for Products is completed')
        print('-'*50,'\n')
    except:
        print("Encoding Product's Categories was Failed")
        os._exit(0)    

    # Mearge product category
    try:
        df_order_v1 = pd.merge(df_order[df_order['order_state']==2], df_product_cat, on='product_id')
        print(f'Dataframe shape : {df_order_v1.shape}')
        # print(f'Dataframe columns name : \n{df_order_v1.columns}\n')
        print('Merging Product catagory is completed')
        print('-'*50,'\n')
    except:
        print("Mearging Product's Categories was Failed")
        os._exit(0)

    # New User ID
    start_newID = 10000
    try:
        df_order_v1, end_newID = CreateNewID(df_order_v1, start_newID, use_cols)
        print(f'New UserID start from {start_newID} to {end_newID}')
        print('Creating New UserID is completed')
        print('-'*50,'\n')
    except:
        print('Creating New UserID was Failed')
        os._exit(0)

    CheckProductID(df_product,df_order_v1)
    # save_csv(df_order_v1, MERGE_DIR, subname='')
    update_AI(df_order_v1, MERGE_DIR)

    # Create Vectors
    try:
        df_full_vector = query_AI(MERGE_DIR)#[full_cols]
        # intial values for Category
        c = 0.0
        df_full_vector = EncodeVector(df_full_vector, cat_cols, c)
        CreateVector(df_full_vector, vector_cols, VECTOR_DIR)
        print('Creating Vectors is completed')
        print('-'*50,'\n')
    except:
        print('Creating Vectors was Failed')
        os._exit(0) 

    # Create Matrixs
    try: # Cosine Similarity
        df_user_vector = query_AI(VECTOR_DIR,'user')
        df_product_vector = query_AI(VECTOR_DIR,'product')
        create_similarity_matrix(df_user_vector, df_product_vector, similarity_cols)

        df_user_item_similarity = query_AI(MATRIX_DIR+'_similarity','user_item')
        df_full_order = query_AI(MERGE_DIR)
        evaluation(df_user_item_similarity, df_full_order, top_n=50)
        print('Creating Similarity Matrix is completed')
        print('-'*50,'\n')
    except:
        print('Creating Similarity Matrix was Failed')
        os._exit(0)

    try: # Euclidean Distances
        df_user_vector = query_AI(VECTOR_DIR+'_user')
        df_product_vector = query_AI(VECTOR_DIR,'product')
        create_distance_matrix(df_user_vector, df_product_vector, distance_cols)

        df_user_item_distance = query_AI(MATRIX_DIR+'_distance','user_item')
        df_full_order = query_AI(MERGE_DIR)
        evaluation(df_user_item_distance, df_full_order, top_n=50)
        print('Creating Distances Matrix is completed')
        print('-'*50,'\n')
    except:
        print('Creating Distances Matrix was Failed')
        os._exit(0)      

def mode_1():
    try:
        df_product = query_dtt('dtt_product')
        df_product = df_product[~df_product['product_id'].isin(test_productID)]
        df_product_cat = query_dtt('dtt_product_category')
        # intial values for Category
        c = 0.0
        df_product_cat = ProductEncode(df_product_cat)
        df_updateProduct_vector = update_NewProduct(df_product, df_product_cat, cat_cols, VECTOR_DIR, c)
        # similarity
        df_user_vector = query_AI(VECTOR_DIR,'user')
        create_similarity_matrix(df_user_vector, df_updateProduct_vector, similarity_cols)
        df_user_item_distance = query_AI(MATRIX_DIR+'_distance','user_item')
        df_full_order = query_AI(MERGE_DIR)
        evaluation(df_user_item_distance, df_full_order, top_n=50)
        # distance
        create_distance_matrix(df_user_vector, df_updateProduct_vector, distance_cols)
        df_user_item_distance = query_AI(MATRIX_DIR+'_distance','user_item')
        df_full_order = query_AI(MERGE_DIR)
        evaluation(df_user_item_distance, df_full_order, top_n=50)

        print('Updating Recommendation Matrix is completed')
        print('-'*50,'\n')
    except:
        print(f'Updating Recommendation Matrix was Failed')
        os._exit(0)  

def mode_2():
    try:
        user_id = int(input('Input your UserID :'))
        recommend_ls = print_user_purchase_and_recommendation(user_id, productID_to_url, top_n=10, url=False)
    except:
        print(f'UserID: {user_id} was not found')
        os._exit(0) 

def mode_3():
    try:
        country_code = int(input('Input your Country Code :'))
        recommend_ls = print_country_purchase_and_recommendation(country_code, productID_to_url, similarity_cols, distance_cols, top_n=10, url=False)
    except:
        print(f'Country Code: {country_code} was not found')
        os._exit(0)  



if __name__ == '__main__':
    print('Select your Mode :\n \
        0 : Creat Recommendation Matrix\n \
        1 : Update New Products and Recommendation Matrix\n \
        2 : List of Recommend Products by userID\n \
        3 : List of Recommend Products by Country')
    input_mode = int(input('Mode :'))
    if input_mode == 0:
        mode_0()
    elif input_mode == 1:
        mode_1()
    elif input_mode == 2:
        mode_2()
    elif input_mode == 3:
        mode_3()
    else:
        print('Input mode is incorrect')