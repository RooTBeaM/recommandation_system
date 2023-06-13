import pandas as pd
import numpy as np
import itertools
import json
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from common import *

def softmax(x, axis = 1):
    return np.exp(x)/np.sum(np.exp(x),axis=axis, keepdims=True)

def compute_similarity(df1, df2, index_col1, index_col2, data_cols):
    similarity_matrix = cosine_similarity(df1[data_cols], df2[data_cols])
    df_similarity = pd.DataFrame(similarity_matrix, columns=df2[index_col2], index=df1[index_col1])
    return df_similarity

def compute_distance(df1, df2, index_col1, index_col2, data_cols):
    distance_matrix = euclidean_distances(df1[data_cols], df2[data_cols])
    df_distance = pd.DataFrame(distance_matrix, columns=df2[index_col2], index=df1[index_col1])
    return df_distance

def recommend_products(df_similarity, customer_id, n=5):
    customer_scores = df_similarity.loc[customer_id].sort_values(ascending=False)
    top_n_products = customer_scores.index[:n].tolist()
    return top_n_products

def evaluation(df_similarity, df_full_order, top_n=5):
    df_similarity.set_index('new_id', inplace=True)
    evaluation_results = []
    for new_id in df_full_order['new_id']:
        recommended_products = recommend_products(df_similarity, new_id, n=top_n)
        has_product_in_top5 = any(str(product) in recommended_products for product in df_full_order[df_full_order['new_id'] == new_id]['product_id'])
        evaluation_results.append(has_product_in_top5)
    percentage = (sum(evaluation_results) / len(evaluation_results)) * 100
    print(f"Percentage of new_id values with at least one product in the top {top_n} recommendations:", round(percentage,2))

def EncodeVector(df_full_vector, cat_cols, c=0):
    df_full_vector.loc[:,'private':'cat_18'] = df_full_vector.loc[:,'private':'cat_18'].applymap(lambda x: c if x == 0 else x)
    df_full_vector.loc[:,'private':'cat_18']
    # mean 
    df_full_vector['order_price_paid'] = df_full_vector['order_price_paid'].div(df_full_vector[['sum_kids', 'sum_adults']].sum(axis=1),axis=0)
    df_full_vector['order_price_paid'] = df_full_vector['order_price_paid']/5000
    # softmax
    df_full_vector[cat_cols] = softmax(df_full_vector[cat_cols].to_numpy())
    df_full_vector[['private', 'group', 'family']] = softmax(df_full_vector[['private', 'group', 'family']].to_numpy())
    # normalize
    df_full_vector[['sum_kids', 'sum_adults']] = df_full_vector[['sum_kids', 'sum_adults']].div(df_full_vector[['sum_kids', 'sum_adults']].sum(axis=1),axis=0)

    return df_full_vector

def CreateVector(df_full_vector, vector_cols, VECTOR_DIR):
    # full_vector
    update_AI(df_full_vector, VECTOR_DIR, subname='fullVector')
    # user_vector
    df_user_vector = df_full_vector.groupby('new_id')[vector_cols].mean()
    df_user_vector.reset_index(inplace=True)
    update_AI(df_user_vector, VECTOR_DIR, subname='user')
    # product_vector
    df_product_vector = df_full_vector.groupby('product_id')[vector_cols].mean()
    df_product_vector.reset_index(inplace=True)
    update_AI(df_product_vector, VECTOR_DIR, subname='product')
    # browser_vector
    df_browser_vector = df_full_vector.groupby('browser')[vector_cols].mean()
    df_browser_vector.reset_index(inplace=True)
    update_AI(df_browser_vector, VECTOR_DIR, subname='browser')
    # platform_vector
    df_platform_vector = df_full_vector.groupby('platform')[vector_cols].mean()
    df_platform_vector.reset_index(inplace=True)
    update_AI(df_platform_vector, VECTOR_DIR, subname='platform')
    # customer_gender_vector
    df_gender_vector = df_full_vector.groupby('customer_gender')[vector_cols].mean()
    df_gender_vector.reset_index(inplace=True)
    update_AI(df_gender_vector, VECTOR_DIR, subname='gender')
    # countryCode_vector
    df_countryCode_vector = df_full_vector.groupby('country_code')[vector_cols].mean()
    df_countryCode_vector.reset_index(inplace=True)
    update_AI(df_countryCode_vector, VECTOR_DIR, subname='countryCode')

def create_similarity_matrix(df_user_vector, df_product_vector, similarity_cols):
    MATRIX_DIR = 'matrix_data_similarity'
    df_user_item_similarity = compute_similarity(df_user_vector, df_product_vector, 'new_id', 'product_id', similarity_cols)
    update_AI(df_user_item_similarity, MATRIX_DIR, subname='user_item', idx = True)
    df_item_item_similarity = compute_similarity(df_product_vector, df_product_vector, 'product_id', 'product_id', similarity_cols)
    update_AI(df_item_item_similarity, MATRIX_DIR, subname='item_item', idx = True)
    # df_user_user_similarity = compute_similarity(df_user_vector, df_user_vector, 'new_id', 'new_id', similarity_cols)
    # update_AI(df_user_user_similarity, MATRIX_DIR, subname='user_user', idx = True)

def create_distance_matrix(df_user_vector, df_product_vector, distance_cols):
    MATRIX_DIR = 'matrix_data_distance'
    df_user_item_distance = compute_distance(df_user_vector, df_product_vector, 'new_id', 'product_id', distance_cols)
    update_AI(df_user_item_distance, MATRIX_DIR, subname='user_item', idx = True)
    df_item_item_distance = compute_distance(df_product_vector, df_product_vector, 'product_id', 'product_id', distance_cols)
    update_AI(df_item_item_distance, MATRIX_DIR, subname='item_item', idx = True)
    # df_user_user_distance = compute_distance(df_user_vector, df_user_vector, 'new_id', 'new_id', distance_cols)
    # update_AI(df_user_user_distance, MATRIX_DIR, subname='user_user', idx = True)

def recommend_top_n(df_similarity, df_distance, customer_id, top_n=10):
    # need load df_user_vector and len(cleanHistory_list) < 10
    VECTOR_DIR = 'vector_data_fullVector'
    df_full_vector = query_AI(VECTOR_DIR, log=False)
    top_50 = list(map(int,recommend_products(df_similarity, customer_id, n=50)))
    history_list = df_full_vector[df_full_vector['new_id']== customer_id]['product_id'].tolist()
    cleanHistory_list = list(itertools.filterfalse(lambda x: x in history_list, top_50))

    customer_scores = df_distance.loc[customer_id].sort_values(ascending=False).index.tolist()
    distance_list = list(map(int,customer_scores))
    recommend_ls = list(itertools.filterfalse(lambda x: x not in cleanHistory_list, distance_list))[:top_n]
    return recommend_ls

def print_user_purchase_and_recommendation(customer_id, productID_to_url, top_n=10, url=True):
    df_product = query_dtt('dtt_product')
    ls = df_product[df_product['is_active']==0]['product_id'].tolist()
    df_user_item_similarity = query_AI('matrix_data_similarity','user_item')
    df_user_item_similarity.drop(columns=map(str, ls), inplace=True, errors='ignore')
    df_user_item_similarity.set_index('new_id', inplace=True)
    df_user_item_distance = query_AI('matrix_data_distance','user_item')
    df_user_item_distance.drop(columns=map(str, ls), inplace=True, errors='ignore')
    df_user_item_distance.set_index('new_id', inplace=True)
    recommend_ls = recommend_top_n(df_user_item_similarity, df_user_item_distance, customer_id, top_n=top_n)
    
    if not url:
        print("User Recommended Products:")
        print(recommend_ls)
        return recommend_ls
    else:
        VECTOR_DIR = 'vector_data_fullVector'
        df_full_vector = query_AI(VECTOR_DIR)
        history_list = df_full_vector[df_full_vector['new_id']== customer_id]['product_id'].tolist()
        
        print("User Purchase History:")
        print_product_links(history_list, productID_to_url)
        print("User Recommended Products:")
        print_product_links(recommend_ls, productID_to_url)

def print_country_purchase_and_recommendation(country_code, productID_to_url, similarity_cols, distance_cols, top_n=10, url=False):
    df_product = query_dtt('dtt_product')
    ls = df_product[df_product['is_active']==0]['product_id'].tolist()
    df_product_vector = query_AI('vector_data_product')
    df_product_vector.drop(index=map(int, ls), inplace=True, errors='ignore')
    df_countryCode_vector =  query_AI('vector_data_countryCode')
    country_vector = df_countryCode_vector[df_countryCode_vector['country_code']==country_code]
    if country_vector.shape[0] == 0:
        print(f'Country Code : {country_code} is not found in DATABASE')
        return None
    else:
        df_item_item_similarity = compute_similarity(df_countryCode_vector, df_product_vector, 'country_code', 'product_id', similarity_cols)
        df_item_item_distance = compute_distance(df_countryCode_vector, df_product_vector, 'country_code', 'product_id', distance_cols)
        top_30 = list(map(int,recommend_products(df_item_item_similarity, country_code, n=30)))
        customer_scores = df_item_item_distance.loc[country_code].sort_values(ascending=False).index.tolist()
        distance_list = list(map(int,customer_scores))
        recommend_ls = list(itertools.filterfalse(lambda x: x not in top_30, distance_list))[:top_n]

    if not url:
        print("User Recommended Products:")
        print(recommend_ls)
        return recommend_ls
    else:
        VECTOR_DIR = 'vector_data_fullVector'
        df_full_vector = query_AI(VECTOR_DIR)
        history_list = df_full_vector[df_full_vector['country_code']== country_code]['product_id'].tolist()
        
        print("User Purchase History:")
        print_product_links(history_list, productID_to_url)
        print("User Recommended Products:")
        print_product_links(recommend_ls, productID_to_url)

def create_recommend_list(mode, similarity_cols, distance_cols, user_cols, top_n=10):
    df_product = query_dtt('dtt_product')
    ls = df_product[df_product['is_active']==0]['product_id'].tolist()
    if mode == 'user':
        df_user_item_similarity = query_AI('matrix_data_similarity','user_item')
        df_user_item_similarity.drop(columns=map(str, ls), inplace=True, errors='ignore')
        df_user_item_similarity.set_index('new_id', inplace=True)
        df_user_item_distance = query_AI('matrix_data_distance','user_item')
        df_user_item_distance.drop(columns=map(str, ls), inplace=True, errors='ignore')
        df_user_item_distance.set_index('new_id', inplace=True)

        VECTOR_DIR = 'vector_data_fullVector'
        df_full_vector = query_AI(VECTOR_DIR, log=False)

        df_newUser = query_AI('merge_data')
        df_newUser = df_newUser.drop_duplicates(subset='new_id')[user_cols]
        recommend_ls = []
        for customer_id in tqdm(df_newUser['new_id']):
            top_50 = list(map(int,recommend_products(df_user_item_similarity, customer_id, n=50)))
            history_list = df_full_vector[df_full_vector['new_id']== customer_id]['product_id'].tolist()
            cleanHistory_list = list(itertools.filterfalse(lambda x: x in history_list, top_50))
            customer_scores = df_user_item_distance.loc[customer_id].sort_values(ascending=False).index.tolist()
            distance_list = list(map(int,customer_scores))
            recommend = list(itertools.filterfalse(lambda x: x not in cleanHistory_list, distance_list))[:top_n]
            recommend_ls.append(json.dumps(recommend))
        df_newUser['recommendation'] = recommend_ls
        update_AI(df_newUser, 'user_reccommand')

    elif mode == 'country':
        df_product_vector = query_AI('vector_data_product')
        df_product_vector.drop(index=map(int, ls), inplace=True, errors='ignore')
        df_countryCode_vector =  query_AI('vector_data_countryCode')
        recommend_ls = []
        for country_code in tqdm(df_countryCode_vector['country_code']):
            country_vector = df_countryCode_vector[df_countryCode_vector['country_code']==country_code]
            if country_vector.shape[0] == 0:
                print(f'Country Code : {country_code} is not found in DATABASE')
                return None
            else:
                df_item_item_similarity = compute_similarity(df_countryCode_vector, df_product_vector, 'country_code', 'product_id', similarity_cols)
                df_item_item_distance = compute_distance(df_countryCode_vector, df_product_vector, 'country_code', 'product_id', distance_cols)
                top_30 = list(map(int,recommend_products(df_item_item_similarity, country_code, n=30)))
                customer_scores = df_item_item_distance.loc[country_code].sort_values(ascending=False).index.tolist()
                distance_list = list(map(int,customer_scores))
                recommend = list(itertools.filterfalse(lambda x: x not in top_30, distance_list))[:top_n]
            recommend_ls.append(json.dumps(recommend))
        df_countryCode_vector['recommendation'] = recommend_ls
        update_AI(df_countryCode_vector[['country_code','recommendation']], 'country_reccommand')
    else:
        print(f'{mode} does not exist.')
