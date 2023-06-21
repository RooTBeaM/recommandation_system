import re
import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.preprocessing import OrdinalEncoder

def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))

def encode_gender(inputString):
    if 'Mr.' == inputString or 'mr.' in inputString:
        return 0
    elif 'Ms.' == inputString or 'ms.' in inputString:
        return 1
    elif 'Mrs.' == inputString or 'mrs.' in inputString:
        return 2
    else:
        return 3

def encode_phone_code(inputFloat, phoneCode_to_id):
    try:
        return phoneCode_to_id[str(int(inputFloat))]
    except:
        print(int(inputFloat))

def encode_order_payment_by(inputString):
    if 'creditcard' == inputString:
        return 1
    elif 'paypal' == inputString:
        return 2
    else:
        return 0
    
def CleanDrop(df_order):
    # rename column : order_product_id >>> product_id
    df_order.rename(columns={'order_product_id': 'product_id'}, inplace=True)

    # drop na
    na_index = df_order[df_order['customer_country'].isna()].index
    df_order = df_order.drop(na_index)

    # drop test
    test_index_v1 = df_order[df_order['customer_email'].map(lambda x: 'test' in str(x) or '@mail.com' in str(x) or '360' in str(x))].index
    df_order = df_order.drop(test_index_v1)

    test_index_v2 = df_order[df_order['customer_email'].map(lambda x: 'mitkung' in str(x) or 'suphattra' in str(x))].index
    df_order = df_order.drop(test_index_v2)

    test_index_v3 = df_order[df_order['customer_firstname'].map(lambda x: 'admin' in str(x) or 'test' in str(x) or 'Thanadol' in str(x) or 'Test' in str(x))].index
    df_order = df_order.drop(test_index_v3)

    test_index_v3 = df_order[df_order['customer_firstname'].map(lambda x: ('asd' in str(x) or 'dsd' in str(x) or 'xx' in str(x)) and not 'Jasdeep' in str(x))].index
    df_order = df_order.drop(test_index_v3)

    # clean spacial characters
    df_order.loc[3627, 'customer_firstname'] = 'Jennyhan'
    df_order['customer_firstname'] = df_order['customer_firstname'].map(lambda x: re.sub('[0-9#$;:]+', '', x))
    df_order['customer_lastname'] = df_order['customer_lastname'].map(lambda x: re.sub('[0-9#$;:]+', '', x))
    df_order['customer_nationality'] = df_order['customer_nationality'].map(lambda x: re.sub('ไทย|Thailand', 'thai', x))
    df_order['customer_nationality'] = df_order['customer_nationality'].map(lambda x : x.lower())

    return df_order


def CleanEncode(df_order, df_order_country):
    # encode country code
    # id_to_countryCode = {i[1][0] : i[1][3] for i in df_order_country.iterrows()}
    countryCode_to_id = {i[1][1] : i[1][0] for i in df_order_country.iterrows()}

    phoneCode_to_id = {}
    countryName_to_id = {i[1][3] : i[1][0] for i in df_order_country.iterrows()}
    for i in df_order_country.iterrows():
        val = i[1][0]
        if len(i[1][2].split(',')) > 1:
            for j in i[1][2].split(','):
                phoneCode_to_id[j] = val
        else:
            phoneCode_to_id[i[1][2]] = val
    
    df_order['customer_gender'] = df_order['customer_gender'].map(lambda x : encode_gender(str(x)))
    # [Mr.,Ms.,Mrs.,nan]
    df_order['customer_country'] = df_order['customer_country'].map(lambda x : countryName_to_id[x] if x else x)

    df_order.fillna(value={'customer_phone_iso': -1, 'customer_phone_code':-1, 'order_payment_by': 0}, inplace=True)
    df_order['customer_phone_iso'] = df_order['customer_phone_iso'].map(lambda x : -1 if x == -1 else countryCode_to_id[x])
    df_order['customer_phone_code'] = df_order['customer_phone_code'].map(lambda x : -1 if x == -1 else encode_phone_code(x, phoneCode_to_id))
    df_order['order_payment_by'] = df_order['order_payment_by'].map(lambda x : encode_order_payment_by(str(x)))

    df_order['customer_phone_iso'] = np.where(df_order['customer_phone_iso']==-1, df_order['customer_country'], df_order['customer_phone_iso'])
    df_order['customer_phone_code'] = np.where(df_order['customer_phone_code']==-1, df_order['customer_country'], df_order['customer_phone_iso'])

    enc = OrdinalEncoder(dtype='int8', encoded_missing_value=-1)
    cat_cols = ['browser', 'platform', 'order_state']
    # browser = ['Android Browser', 'AppleWebKit', 'Chrome', 'Edge', 'Firefox','MSIE', 'Opera Next', 'Safari', 'SamsungBrowser', 'Vivaldi', nan]
    # platform = ['Android', 'Chrome OS', 'Linux', 'Macintosh', 'Windows', 'iPad','iPhone', nan]
    # order_state = ['cancelled', 'detail_success', 'payment_success']
    df_order[cat_cols] = enc.fit_transform(df_order[cat_cols])

    # change dtype to int
    int_cols = ['customer_phone_iso', 'customer_phone_code','order_price_paid', 'customer_id']
    df_order['customer_phone_iso'] = np.where(df_order['customer_phone_iso']==-1, df_order['customer_country'], df_order['customer_phone_iso'])
    df_order['customer_phone_code'] = np.where(df_order['customer_phone_code']==-1, df_order['customer_country'], df_order['customer_phone_iso'])
    df_order[int_cols] = df_order[int_cols].astype('int64')

    # convert to datetime
    df_order[['order_departure_date','date_create']] = df_order[['order_departure_date','date_create']].apply(pd.to_datetime)

    df_order['booked_days'] =  df_order['order_departure_date'] - df_order['date_create']
    df_order['booked_days'] = df_order['booked_days'].map(lambda x: x.days if x.days >= 0 else 0)

    df_order['departure_year'] = df_order['order_departure_date'].map(lambda x:x.year)
    df_order['departure_month'] = df_order['order_departure_date'].map(lambda x:x.month)
    df_order['departure_week'] = df_order['order_departure_date'].map(lambda x:x.week)
    df_order['departure_day'] = df_order['order_departure_date'].map(lambda x:x.day)

    df_order['departure_DayofYear'] = df_order['order_departure_date'].map(lambda x:x.day_of_year)
    df_order['departure_DayofWeek'] = df_order['order_departure_date'].map(lambda x:x.day_of_week)

    # Majority Vote for country code
    # df_order['country_code'] = df_order[['customer_country','customer_phone_iso','customer_phone_code']].mode(axis=1)
    df_order['country_code'] = df_order['customer_country']

    # sum of kid  and adult
    df_order['sum_kids'] = df_order['order_quantity_infant'] + df_order['order_quantity_children']
    df_order['sum_adults'] = df_order['order_quantity_adult'] + df_order['order_quantity_elder']

    # creeate new columns
    df_order['private'] = np.where((df_order['sum_kids'] == 0) & (df_order['sum_adults'] <= 2), 1, 0)
    df_order['group'] = np.where((df_order['sum_kids'] == 0) & (df_order['sum_adults'] > 2), 1, 0)
    df_order['family'] = np.where((df_order['sum_kids'] > 0) & (df_order['sum_adults'] > 0), 1, 0)

    return df_order

def ProductEncode(df_product_cat):
    # rename column : order_product_id >>> product_id
    df_product_cat.rename(columns={'order_product_id': 'product_id'}, inplace=True)
    # Perform one-hot encoding
    one_hot_encoded = pd.get_dummies(df_product_cat['category_id'], prefix='cat')
    # Group by 'product_id' and sum the one-hot encoded columns
    df_grouped = one_hot_encoded.groupby(df_product_cat['product_id']).sum()
    # Reset the index to make 'product_id' a column again
    df_grouped = df_grouped.reset_index()
    # Drop duplicate rows based on 'product_id'
    df_product_cat = df_product_cat.drop_duplicates(subset='product_id')
    # Merge the grouped DataFrame back to the original DataFrame
    df_product_cat = pd.merge(df_product_cat.drop(columns=['category_id']), df_grouped, on='product_id')
    return df_product_cat

def CreateNewID(df_user_id, start_newID, use_cols):
    # fix customer_id is 0 or 23
    df_user_id['new_id'] = df_user_id['customer_id']
    df_user_id['new_firstname'] = df_user_id['customer_firstname'].str.lower()
    df_user_id['new_lastname'] = df_user_id['customer_lastname'].str.lower()
    df_user_id['new_email'] = df_user_id['customer_email'].str.lower()

    email_dict = df_user_id['new_email'].value_counts()
    del email_dict['support@daytriptour.com']

    # Replace customer_id [0,23]
    for i in tqdm(email_dict.keys()):
        x = df_user_id.query(f'new_email == "{str(i)}"')['customer_id'].unique().tolist()
        if 0 in x: x.remove(0)
        if 23 in x: x.remove(23)
        if len(x) > 0:
            val_id = max(x)
            idx = df_user_id.query(f'new_email == "{str(i)}"').index
            for j in idx:
                if df_user_id.loc[j]['customer_id'] in [0,23]:
                    # customer_id more than one select latest registration ID
                    df_user_id.loc[j,['new_id']] = val_id
        else:
            idx = df_user_id.query(f'new_email == "{str(i)}"').index
            for j in idx:
                df_user_id.loc[j,['new_id']] = start_newID
            start_newID+=1

    email_dict_daytriptour = df_user_id.query('new_email == "support@daytriptour.com"')['new_lastname'].value_counts()
    print(f'New UserID start from 10000 to {start_newID}')
    
    for i in tqdm(email_dict_daytriptour.keys()):
        x = df_user_id.query(f'new_lastname == "{str(i)}" & new_email == "support@daytriptour.com"')['new_firstname'].unique().tolist()
        if len(x) == 1:
            idx = df_user_id.query(f'new_lastname == "{str(i)}" & new_email == "support@daytriptour.com"').index
            for j in idx:
                df_user_id.loc[j,['new_id']] = start_newID
            start_newID+=1
        else:
            for k in x:
                idx = df_user_id.query(f'new_lastname == "{str(i)}" & new_firstname == "{str(k)}" & new_email == "support@daytriptour.com"').index
                for j in idx:
                    df_user_id.loc[j,['new_id']] = start_newID
                start_newID+=1

    return df_user_id[use_cols], start_newID-1
