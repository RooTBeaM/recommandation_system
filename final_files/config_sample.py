# DB schema name # change DB name her
DB_DTT = 'dtt'
DB_AI = 'daytriptour_ai'

config = {
  'user': 'root',
  'password': 'xxx',# change here!
  'host': 'xxx',# change here!
  'port': '3306',# change here!
  'raise_on_warnings': True
}

config_dtt = {
  'user': 'root',
  'password': 'xxx',# change here!
  'host': 'xxx',# change here!
  'port': '3306',# change here!
  'database': DB_DTT,
  'raise_on_warnings': True
}

config_ai = {
  'user': 'root',
  'password': 'xxx',# change here!
  'host': 'xxx',# change here!
  'port': '3306',# change here!
  'database': DB_AI,
  'raise_on_warnings': True
}

# change API key for pyowm here!
api_key = 'xxx'

# directory
CLEAN_DIR = 'clean_data'
VECTOR_DIR = 'vector'
MATRIX_DIR = 'matrix'

user_cols = [
    'customer_id','new_id','customer_firstname', 'customer_lastname', 'customer_email', 'customer_gender', 'customer_country']
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
    'booked_days', 'departure_year', 'departure_month', 'departure_week', 'departure_day',
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
    # 'booked_days',  
    'order_price_paid', 
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
    # 'booked_days', 
    'order_price_paid', 
    'sum_kids','sum_adults', 
    'private', 'group', 'family', 
    'cat_1', 'cat_2', 'cat_3','cat_4', 'cat_5', 'cat_6', 'cat_7', 'cat_8', 'cat_9', 'cat_10',
    'cat_11', 'cat_12', 'cat_13', 'cat_14', 'cat_15', 'cat_16', 'cat_17','cat_18']
cat_cols = [
    'cat_1', 'cat_2', 'cat_3', 'cat_4', 'cat_5', 'cat_6', 'cat_7', 'cat_8', 'cat_9',
    'cat_10', 'cat_11', 'cat_12', 'cat_13', 'cat_14', 'cat_15', 'cat_16','cat_17', 'cat_18']
month_cols = ['m_'+str(x) for x in range(1,13)]

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




