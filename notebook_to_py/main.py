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

df_product = pd.read_csv('../raw_csv/dtt_product.csv')
df_product = df_product[~df_product['product_id'].isin(test_productID)]

# URLs
productID_to_url = {i[1][0] : 'www.daytriptour.com/trip/' + i[1][2] for i in df_product.iterrows()}

def mode_0():
    # load data
    df_user = pd.read_csv('../raw_csv/dtt_users.csv')
    df_country = pd.read_csv('../raw_csv/dtt_country.csv')[['country_id','country_code','country_phonecode','country_name']]
    df_order = pd.read_csv('../raw_csv/dtt_order.csv')[order_col]
    df_product_cat = pd.read_csv('../raw_csv/dtt_product_category.csv')
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
        print('Encoding Data for Orders is completed')
        print(f'Dataframe shape : {df_order.shape}')
        print(f'Dataframe columns name : \n{df_order.columns}\n')
    except:
        print('Encoding in Cleaning Process was Failed')
        os._exit(0)

    CLEAN_DIR = './clean_data/'
    save_csv(df_order, CLEAN_DIR, subname='')
    print('-'*50,'\n')

    # Product category
    try:
        df_product_cat = ProductEncode(df_product_cat)
        print(f'Total products : {len(df_product_cat)}')
        print('Encoding Data for Products is completed')
        print(f'Dataframe shape : {df_product_cat.shape}')
        print(f'Dataframe columns name : \n{df_product_cat.columns}\n')
    except:
        print("Encoding Product's Categories was Failed")
        os._exit(0)    

    # Mearge product category
    try:
        df_order_v1 = pd.merge(df_order[df_order['order_state']==2], df_product_cat, on='product_id')
        print('Merging Product catagory is completed')
        print(f'Dataframe shape : {df_order_v1.shape}')
        # print(f'Dataframe columns name : \n{df_order_v1.columns}\n')
    except:
        print("Mearging Product's Categories was Failed")
        os._exit(0)    

    # New User ID
    start_newID = 10000
    try:
        df_order_v1, end_newID = CreateNewID(df_order_v1, start_newID, use_cols)
        print('Creating New UserID is completed')
        print(f'New UserID start from {start_newID} to {end_newID}')
    except:
        print('Creating New UserID was Failed')
        os._exit(0)    

    MERGE_DIR = './merge_data/'
    df_full_order = pd.read_csv(select_csv_path(MERGE_DIR))
    CheckProductID(df_product,df_full_order)
    save_csv(df_full_order, MERGE_DIR, subname='')
    print('-'*50,'\n')

    # Create Vectors
    VECTOR_DIR = './vector_data/'
    try:
        df_full_vector = pd.read_csv(select_csv_path(MERGE_DIR))[full_cols]

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
    MATRIX_DIR = './matrix_data/'
    try: # Cosine Similarity
        df_user_vector = pd.read_csv(select_csv_path(VECTOR_DIR+'user/'))
        df_product_vector = pd.read_csv(select_csv_path(VECTOR_DIR+'product/'))
        create_similarity_matrix(df_user_vector, df_product_vector, similarity_cols)
        print('Creating Similarity Matrix is completed')

        df_user_item_similarity = pd.read_csv(select_csv_path(MATRIX_DIR+'similarity/user_item/'))
        df_full_order = pd.read_csv(select_csv_path(MERGE_DIR))
        evaluation(df_user_item_similarity, df_full_order, top_n=50)
        print('-'*50,'\n')
    except:
        print('Creating Similarity Matrix was Failed')
        os._exit(0)

    try: # Euclidean Distances
        df_user_vector = pd.read_csv(select_csv_path(VECTOR_DIR+'user/'))
        df_product_vector = pd.read_csv(select_csv_path(VECTOR_DIR+'product/'))
        create_distance_matrix(df_user_vector, df_product_vector, distance_cols)

        df_user_item_distance = pd.read_csv(select_csv_path(MATRIX_DIR+'distance/user_item/'))
        df_full_order = pd.read_csv(select_csv_path(MERGE_DIR))
        evaluation(df_user_item_distance, df_full_order, top_n=50)
        print('-'*50,'\n')
    except:
        print('Creating Distances Matrix was Failed')
        os._exit(0)    

def mode_1():
    try:
        input_id = int(input('UserID :'))
        print_user_purchase_and_recommendation(input_id, productID_to_url, top_n=10, url=False)
    except:
        print(f'UserID: {input_id} was not found')
        os._exit(0)   


if __name__ == '__main__':
    print('0 : creat recommendations matrix\n1 : test')
    input_mode = int(input('Mode :'))
    if input_mode == 0:
        mode_0()
    elif input_mode == 1:
        mode_1()
    else:
        print('Input mode is incorrect')