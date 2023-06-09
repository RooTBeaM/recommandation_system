import re
import pandas as pd

from vector import *
from common import *

def update_NewProduct(df_product, df_product_cat, cat_cols, VECTOR_DIR, c=0):
    df_product_vector = query_AI('vector_data_product')
    product_ids_not_present = ~df_product['product_id'].isin(df_product_vector['product_id'])
    product_ids_list = df_product.loc[product_ids_not_present, 'product_id'].tolist()
    print("Product IDs not present in Order:" , len(product_ids_list))
    product_ids_list.sort()
    print(product_ids_list)
    # encode
    df_newID = df_product_cat[df_product_cat['product_id'].isin(product_ids_list)]
    df_newID.loc[:,cat_cols] = df_newID.loc[:,cat_cols].applymap(lambda x: c if x == 0 else x)
    df_newID[cat_cols] = softmax(df_newID[cat_cols].to_numpy())
    # vector
    df_item_item_similarity = compute_similarity(df_newID, df_product_vector, 'product_id', 'product_id', cat_cols)
    df_item_item_distance = compute_distance(df_newID, df_product_vector, 'product_id', 'product_id', cat_cols)
    df = pd.DataFrame(columns=['product_id','booked_days','order_price_paid','sum_kids','sum_adults','private','group','family'])
    for i in df_newID['product_id']:
        rec_ls = recommend_top_n(df_item_item_similarity, df_item_item_distance, i, 10)
        pgf = df_product_vector[df_product_vector['product_id'].isin(rec_ls)][['booked_days','order_price_paid','sum_kids','sum_adults','private','group','family']].mean()
        pgf['product_id'] = i
        df = pd.concat([df,pgf.to_frame().T])
    df['product_id'] = df['product_id'].astype(int)
    df_newID = df.merge(df_newID, how='left', on='product_id')
    # update df_product_vector
    df_newID = pd.concat([df_product_vector,df_newID]).sort_values(by=['product_id'])
    # save_csv(df_newID, VECTOR_DIR, subname='product')
    update_AI(df_newID, VECTOR_DIR, subname='product')
    return df_newID
    