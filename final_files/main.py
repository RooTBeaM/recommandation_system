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

def Create_Recommedation():
    # Load data from database
    print('>>>> Starting to create and update ALL TABLES')
    df_country = query_dtt('dtt_country')[['country_id','country_code','country_phonecode','country_name']]
    df_order = query_dtt('dtt_order')[order_col]
    df_product_cat = query_dtt('dtt_product_category')
    print('-'*15, 'Data Loaded', '-'*15)
    print(f'Total Orders : {len(df_order)}')

    # Clean data
    df_order = df_order[df_order['order_state']=='payment_success']
    print(f'Total payment_success Orders : {len(df_order)}')
    df_order = CleanDrop(df_order)
    df_order = CleanEncode(df_order, df_country)
    print(f'Final Cleaning shape : {df_order.shape}')
    print(f'Dataframe columns name : \n{df_order.columns}\n')

    # Encode
    df_product_cat = ProductEncode(df_product_cat)
    df_order_v1 = pd.merge(df_order, df_product_cat, on='product_id')
    print(f'Final Merging shape : {df_order_v1.shape}')

    # New User ID
    start_newID = 10000
    df_order_v1, end_newID = CreateNewID(df_order_v1, start_newID, use_cols)
    # Update table
    update_AI(df_order_v1, CLEAN_DIR)
    print('Cleaning Process is completed')
    print('-'*50)

    # Check products_id not in Orders
    CheckProductID(df_order_v1)

    # Create Vectors
    df_full_vector = query_AI(CLEAN_DIR)
    # intial values for Category(c) and Count(k)
    c = 0.0
    k = 1
    df_full_vector = EncodeVector(df_full_vector, cat_cols, c)
    CreateVector(df_full_vector, vector_cols, VECTOR_DIR)
    print('Creating Vectors is completed')
    print('-'*50)

    # Create Matrixs
    df_user_vector = query_AI(VECTOR_DIR,'user')
    df_product_vector = query_AI(VECTOR_DIR,'product')
    df_full_order = query_AI(CLEAN_DIR)
        # Cosine Similarity
    create_similarity_matrix(df_user_vector, df_product_vector, similarity_cols)
    df_user_item_similarity = query_AI(MATRIX_DIR+'_similarity','user_item')
    evaluation(df_user_item_similarity, df_full_order, top_n=50, ascending=False)
    print('Creating Similarity Matrix is completed')
    print('-'*50)
        # Euclidean Distances
    create_distance_matrix(df_user_vector, df_product_vector, distance_cols)
    df_user_item_distance = query_AI(MATRIX_DIR+'_distance','user_item')
    evaluation(df_user_item_distance, df_full_order, top_n=50, ascending=True)
    print('Creating Distances Matrix is completed')
    print('-'*50)

    # Update New Products and Recommendation Matrix
    df_product = query_dtt('dtt_product')
    df_product = df_product[~df_product['product_id'].isin(test_productID)]
    df_product_cat = query_dtt('dtt_product_category')

    df_product_cat = ProductEncode(df_product_cat)
    updated = update_NewProduct(df_product, df_product_cat, cat_cols, VECTOR_DIR, c)
    if updated:
        df_product_vector = query_AI(VECTOR_DIR,'product')
            # Cosine Similarity
        create_similarity_matrix(df_user_vector, df_product_vector, similarity_cols)
        df_user_item_distance = query_AI(MATRIX_DIR+'_distance','user_item')
        evaluation(df_user_item_distance, df_full_order, top_n=50, ascending=False)
            # Euclidean Distances
        create_distance_matrix(df_user_vector, df_product_vector, distance_cols)
        df_user_item_distance = query_AI(MATRIX_DIR+'_distance','user_item')
        evaluation(df_user_item_distance, df_full_order, top_n=50, ascending=True)

        print('Updating Recommendation Matrix is completed')
        print('-'*50)
    else:
        print('All Products already updated')

    # Create the recommendation list
    create_recommend_list('country', similarity_cols, distance_cols, user_cols,top_n=10)
    create_recommend_list('user', similarity_cols, distance_cols, user_cols,top_n=10)


if __name__ == '__main__':
    Create_Recommedation()