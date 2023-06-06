from pathlib import Path
from datetime import datetime
from glob import glob
import os

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

def CheckProductID(df_product, df_order_v1):
    product_ids_not_present = ~df_product['product_id'].isin(df_order_v1['product_id'])
    product_ids_list = df_product.loc[product_ids_not_present, 'product_id'].tolist()
    print("Product IDs not present in df_product_matrix:" , len(product_ids_list))
    print(product_ids_list)

def print_product_links(product_ls, productID_to_url):
    # print("Product Links:")
    for product_id in product_ls:
        print(productID_to_url[product_id])