import re
import pandas as pd

from vector import *
from common import *
from config import month_cols

def update_NewProduct(df_product, df_product_cat, cat_cols, VECTOR_DIR, c=0):
    df_product_vector = query_AI('vector_data_product')
    df_month_vector = query_AI('vector_data_month')
    product_ids_not_present = ~df_product['product_id'].isin(df_product_vector['product_id'])
    product_ids_list = df_product.loc[product_ids_not_present, 'product_id'].tolist()
    print("Product IDs not present in Order:" , len(product_ids_list))
    if len(product_ids_list) == 0:
        return False
    else:
        # encode
        df_newID = df_product_cat[df_product_cat['product_id'].isin(product_ids_list)]
        df_newID.loc[:,cat_cols] = df_newID.loc[:,cat_cols].applymap(lambda x: c if x == 0 else x)
        df_newID.loc[:,cat_cols] = softmax(df_newID[cat_cols].to_numpy())
        # vector
        df_item_item_similarity = compute_similarity(df_newID, df_product_vector, 'product_id', 'product_id', cat_cols)
        df_item_item_distance = compute_distance(df_newID, df_product_vector, 'product_id', 'product_id', cat_cols)
        df_item = pd.DataFrame(columns=['product_id','order_price_paid','sum_kids','sum_adults','private','group','family'])
        df_month = pd.DataFrame(columns=df_month_vector.columns)

        for i in df_newID['product_id']:
            rec_ls = recommend_top_n(df_item_item_similarity, df_item_item_distance, i, 10)
            vector_mean = df_product_vector[df_product_vector['product_id'].isin(rec_ls)][['order_price_paid','sum_kids','sum_adults','private','group','family']].mean()
            vector_mean['product_id'] = i
            df_item = pd.concat([df_item,vector_mean.to_frame().T])

            month_mean = df_month_vector[df_month_vector['product_id'].isin(rec_ls)][month_cols].mean()
            month_mean['product_id'] = i
            df_month = pd.concat([df_month,month_mean.to_frame().T])

        df_item['product_id'] = df_item['product_id'].astype(int)
        df_month['product_id'] = df_month['product_id'].astype(int)

        df_newID = df_item.merge(df_newID, how='left', on='product_id')
        df_newID = pd.concat([df_product_vector,df_newID]).sort_values(by=['product_id'])
        update_AI(df_newID, VECTOR_DIR, subname='product')

        df_newID_month = pd.concat([df_month_vector,df_month]).sort_values(by=['product_id'])
        update_AI(df_newID_month, VECTOR_DIR, subname='month')
        return True
    
