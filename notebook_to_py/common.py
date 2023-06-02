from pathlib import Path
from datetime import datetime
from glob import glob

def save_csv(df, dir, subname='', idx=False):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_dir = dir+subname
    full_path = f'{full_dir}/{time}.csv'
    Path(full_dir).mkdir(parents=True, exist_ok=True)
    # print(f'{full_dir}{time}.csv')
    df.to_csv(full_path, index=idx)
    print(f'SAVED CSV : {full_path}')

def select_csv_path(dir):
    dirFiles = [Path(x).name for x in glob(f'{dir}*.csv')]
    if dirFiles !=[]:
        dirFiles.sort(reverse=True)
        filePath = dir+dirFiles[0]
        print(f'READ CSV : {filePath}')
    else:
        print('CSV File was not found')
    return Path(filePath)

def CheckProductID(df_product, df_order_v1):
    # Check which product IDs are not present in df_product_matrix
    product_ids_not_present = ~df_product['product_id'].isin(df_order_v1['product_id'])
    # Get the list of product IDs not present in df_product_matrix
    product_ids_list = df_product.loc[product_ids_not_present, 'product_id'].tolist()
    # Print the list of product IDs not present
    print("Product IDs not present in df_product_matrix:" , len(product_ids_list))
    print(product_ids_list)