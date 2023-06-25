import pandas as pd
import pyowm
from geopy.geocoders import Nominatim
from meteostat import Stations, Daily

from config import *
from common import *

def create_station(df_province):
    # Retrieve the list of weather stations in Thailand
    stations = Stations()
    stations = stations.region("TH").fetch()
    stations = stations.reset_index(drop=False)
    # Display the station IDs and names
    df_stations = stations[['id', 'name', 'latitude', 'longitude']]
    df_stations = df_stations.rename(columns={'id': 'stations_id', 'name': 'stations_name'})
    # Create a geocoder object
    geolocator = Nominatim(user_agent='my_agent')
    # Define a function to get the province and country from coordinates
    def get_location_info(latitude, longitude):
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        if location is not None:
            address = location.raw.get('address', {})
            province = address.get('state', '')
            country = address.get('country', '')
            return province, country
        else:
            return '', ''
    df_stations[['province', 'country']] = df_stations.apply(lambda row: pd.Series(get_location_info(row['latitude'], row['longitude'])), axis=1)
    # df_stations = pd.read_csv('stations.csv')
    df_stations['province'] = df_stations['province'].str.replace('จังหวัด', '')
    df_stations.loc[df_stations['stations_name'] == 'Mae Hong Son', 'province'] = 'แม่ฮ่องสอน'
    df_stations.loc[df_stations['stations_name'] == 'Chiang Mai', 'province'] = 'เชียงใหม่'
    df_stations.loc[df_stations['stations_name'] == 'Lamphun', 'province'] = 'ลำพูน'
    df_stations.loc[df_stations['stations_name'] == 'Nakhon Phanom Agromet / Ban Namuang', 'province'] = 'นครพนม'
    df_stations.loc[df_stations['stations_name'] == 'Bangkok Pilot', 'province'] = 'กรุงเทพมหานคร'
    df_stations.loc[df_stations['stations_name'] == 'Aranyaprathet', 'province'] = 'สระแก้ว'
    df_stations.loc[df_stations['stations_name'] == 'Taphao / Ban Khlong Kao', 'province'] = 'สมุทรสงคราม'
    df_stations = df_stations.merge(df_province, left_on='province', right_on='province_th', how='left')
    df_stations = df_stations[['stations_id','latitude','longitude','stations_name','province_en','province_th','province_id']]
    update_AI(df_stations,'stations')
    return df_stations

def get_province_forecast(api_key, df_clean, df_province):
    # Openweathermap API key
    owm = pyowm.OWM(api_key)
    # Create an empty DataFrame to store the combined forecast
    combined_forecast_df = pd.DataFrame(columns=['province', 'date', 'rainfall'])
    # List of places to forecast
    places = df_clean['province_en'].unique()
    # Iterate over each place and retrieve the forecast
    for place in places:
        mgr = owm.weather_manager()
        forecast = mgr.forecast_at_place(place, '3h')
        # Create a list to store forecast data
        forecast_data = []
        # Store the weather forecast data
        for weather in forecast.forecast:
            forecast_data.append({
                'Time': weather.reference_time('iso'),
                'Status': weather.status,
                'Rain volume': weather.rain
            })
        place_forecast_df = pd.DataFrame(forecast_data)
        # Extract the date and time from the 'Time' column
        place_forecast_df['DateTime'] = pd.to_datetime(place_forecast_df['Time'])
        place_forecast_df['Date'] = place_forecast_df['DateTime'].dt.date
        place_forecast_df['Time'] = place_forecast_df['DateTime'].dt.time
        # Group the data by date and perform voting for rainfall status
        place_forecast_df = (
            place_forecast_df[place_forecast_df['Time'].between(pd.to_datetime('06:00').time(), pd.to_datetime('18:00').time())]
            .groupby('Date')['Rain volume']
            .apply(lambda x: 1 if any(x) else 0)
            .reset_index()
        )
        place_forecast_df.columns = ['date', 'rainfall']
        # Add the 'Place' column to the forecast DataFrame
        place_forecast_df['province'] = place
        # Append the place forecast to the combined forecast DataFrame
        combined_forecast_df = pd.concat([combined_forecast_df, place_forecast_df], ignore_index=True)
    # Convert 'Date' column to datetime data type
    combined_forecast_df['date'] = pd.to_datetime(combined_forecast_df['date'])
    # Select the forecast for the next 3 days
    today = pd.to_datetime('today').date()
    next_3_days = pd.date_range(start=today, periods=3)
    selected_forecast = combined_forecast_df[combined_forecast_df['date'].isin(next_3_days)]
    # Group the data by province and perform voting for rainfall status
    province_forecast = selected_forecast.groupby('province')['rainfall'].apply(lambda x: x.mode()[0]).reset_index()
    province_forecast.columns = ['province', 'rainfall_forecast']
    province_forecast = pd.merge(province_forecast, df_province[['province_en', 'province_id']], left_on='province', right_on='province_en', how='left')
    return province_forecast

# Function to get rainfall for a specific date and province with weighted voting
def get_rainfall(date, province_id, df_stations):
    # Get the weather stations for the province
    stations = df_stations[df_stations['province_id'] == province_id]['stations_id'].tolist()
    if len(stations) > 1:
        # If multiple stations, use weighted voting to determine rainfall
        votes = []
        weights = []
        for station in stations:
            data = Daily(station, date, date)
            data = data.fetch()
            if len(data) > 0:
                prcp = data['prcp'].iloc[0]
                if prcp > 0:
                    votes.append(1)
                else:
                    votes.append(0)
                weights.append(prcp)

        if len(votes) > 0:
            weighted_vote = sum([vote * weight for vote, weight in zip(votes, weights)])
            weighted_sum = sum(weights)
            if weighted_sum != 0:
                rainfall = 1 if weighted_vote / weighted_sum > 0 else 0
            else:
                rainfall = 0
        else:
            rainfall = 0
    elif len(stations) == 1:
        # If single station, retrieve rainfall directly
        data = Daily(stations[0], date, date)
        data = data.fetch()
        rainfall = 1 if len(data) > 0 and data['prcp'].iloc[0] > 0 else 0
    else:
        rainfall = 0
    return rainfall

def get_recommended_weather_products():
    df_product = query_dtt('dtt_product')[['product_id', 'province_id']]
    df_province = query_dtt('dtt_area')
    df_province['province_en'] = df_province['province_en'].str.replace('-', ' ')
    df_province['province_th'] = df_province['province_th'].str.replace(' ', '')
    df_province = df_province[['province_id', 'province_th', 'province_en']].drop_duplicates('province_id')

    df_clean = query_AI('clean_data')[['product_id', 'order_departure_date']]
    df_clean = df_clean.merge(df_product, on='product_id', how='left')
    df_clean = df_clean.merge(df_province, on='province_id', how='left')
    province_forecast = get_province_forecast(api_key, df_clean, df_province)

    try:
        df_stations = query_AI('stations')
    except:
        print('No Station Table was found, Creating...')
        df_stations = create_station(df_province)

    df_clean['rainfall'] = df_clean.apply(lambda row: get_rainfall(row['order_departure_date'], row['province_id'], df_stations), axis=1)
    
    history_rainfall_product = df_clean.groupby('product_id')['rainfall'].agg(rainy_days='sum', non_rainy_days=lambda x: len(x) - sum(x)).reset_index()
    history_rainfall_product = pd.merge(history_rainfall_product, df_product[['product_id', 'province_id']], on='product_id', how='left')

    # Merge the two DataFrames based on 'province_id'
    merged_data = pd.merge(province_forecast, history_rainfall_product, on='province_id', how='left')
    # Filter products based on the rainfall forecast
    rainy_products = merged_data.loc[merged_data['rainfall_forecast'] == 1]
    non_rainy_products = merged_data.loc[merged_data['rainfall_forecast'] == 0]
    # Check if rainy_days is greater than non_rainy_days for each product
    rainy_products = rainy_products.loc[rainy_products['rainy_days'] >= rainy_products['non_rainy_days']]
    non_rainy_products = non_rainy_products.loc[non_rainy_products['rainy_days'] <= non_rainy_products['non_rainy_days']]
    # Combine product_ids from rainy and non-rainy products
    recommended_weather_products = rainy_products['product_id'].tolist() + non_rainy_products['product_id'].tolist()
    recommended_weather_products = [int(x) for x in recommended_weather_products]
    return recommended_weather_products

