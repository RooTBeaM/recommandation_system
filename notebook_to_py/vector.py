import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from common import save_csv

def softmax(x, axis = 1):
    return np.exp(x)/np.sum(np.exp(x),axis=axis, keepdims=True)

def compute_similarity(df1, df2, index_col1, index_col2, data_cols):
    similarity_matrix = cosine_similarity(df1[data_cols], df2[data_cols])
    similarity_df = pd.DataFrame(similarity_matrix, columns=df2[index_col2], index=df1[index_col1])
    return similarity_df

def compute_distance(df1, df2, index_col1, index_col2, data_cols):
    distance_matrix = euclidean_distances(df1[data_cols], df2[data_cols])
    distance_df = pd.DataFrame(distance_matrix, columns=df2[index_col2], index=df1[index_col1])
    return distance_df

def recommend_products(similarity_df, customer_id, n=5):
    customer_scores = similarity_df.loc[customer_id].sort_values(ascending=False)
    top_n_products = customer_scores.index[:n].tolist()
    return top_n_products

def evaluation(similarity_df, df_users, top_n=5):
    evaluation_results = []
    for new_id in df_users['new_id']:
        recommended_products = recommend_products(similarity_df, new_id, n=top_n)
        has_product_in_top5 = any(product in recommended_products for product in df_users[df_users['new_id'] == new_id]['order_product_id'])
        evaluation_results.append(has_product_in_top5)
    percentage = (sum(evaluation_results) / len(evaluation_results)) * 100
    return percentage

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
# user_vector
    df_user_vector = df_full_vector.groupby('new_id')[vector_cols].mean()
    df_user_vector.reset_index(inplace=True)
    save_csv(df_user_vector, VECTOR_DIR, subname='user')

    # # product_vector
    df_product_vector = df_full_vector.groupby('product_id')[vector_cols].mean()
    df_product_vector.reset_index(inplace=True)
    save_csv(df_product_vector, VECTOR_DIR, subname='product')

    # # browser_vector
    df_browser_vector = df_full_vector.groupby('browser')[vector_cols].mean()
    df_browser_vector.reset_index(inplace=True)
    save_csv(df_browser_vector, VECTOR_DIR, subname='browser')

    # # platform_vector
    df_platform_vector = df_full_vector.groupby('platform')[vector_cols].mean()
    df_platform_vector.reset_index(inplace=True)
    save_csv(df_platform_vector, VECTOR_DIR, subname='platform')

    # # customer_gender_vector
    df_gender_vector = df_full_vector.groupby('customer_gender')[vector_cols].mean()
    df_gender_vector.reset_index(inplace=True)
    save_csv(df_gender_vector, VECTOR_DIR, subname='gender')

    # # countryCode_vector
    df_countryCode_vector = df_full_vector.groupby('country_code')[vector_cols].mean()
    df_countryCode_vector.reset_index(inplace=True)
    save_csv(df_countryCode_vector, VECTOR_DIR, subname='countryCode')

    
