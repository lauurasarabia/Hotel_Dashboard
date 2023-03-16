import pandas as pd
import seaborn as sns
import datetime
import math
import numpy as np


#Function 1
def read_concat_csv(file1, file2, file3, file4):
    """
    Read and concat dataframes vertically
    """
    df1 = pd.read_csv(f"./data/{file1}")
    df2 = pd.read_csv(f"./data/{file2}")
    df3 = pd.read_csv(f"./data/{file3}")
    df4 = pd.read_csv(f"./data/{file4}")

    reservations = pd.concat([df1, df2, df3, df4], axis=0, ignore_index=True)
    return reservations

#Function 2
def nights_counter(df):
    """
    Count how many nights the customer has stayed at the hotel
    adding a new column to DataFrame
    """
    nights_list = []

    for index, row in df.iterrows():
        arrival_date = datetime.datetime.strptime(row['arrival'], '%Y-%m-%d')
        departure_date = datetime.datetime.strptime(row['departure'], '%Y-%m-%d')
        nights = (departure_date - arrival_date).days
        nights_list.append(nights)

    df['nights'] = nights_list
    return df

#Function 3
def room_not_assigned(df, column):
    """
    Identifies cancelled reservations and insert 'not_assigned' in room_id column as they have not been assigned
    """
    cancelled_rows = df[f'{column}'] == 'Cancelled'
    df.loc[cancelled_rows, 'room_id'] = df.loc[cancelled_rows, 'room_id'].fillna('NOT_ASSIGNED')
    return df

#Function 4
def convert_to_int(df, column):
    """
    Converts column to int64 data type, ignoring not_assigned values.
    """
    df[f'{column}'] = pd.to_numeric(df[f'{column}'], errors='coerce').astype('Int64')
    df[f'{column}'] = df[f'{column}'].apply(lambda x: str(x) if pd.notna(x) else 'NOT_ASSIGNED')
    return df

#Function 5
def round_amount_columns(df):
    """
    Round all amount columns to 2 decimals
    """
    for col in df.columns:
        if 'amount' in col:
            df[col] = df[col].round(2)
    return df

#Function 6
def read_continents(file):
    """
    Reads continents file and keeps only the columns we need
    """
    continents = pd.read_csv(f"./data/{file}")

    continents.drop(['sub-region', 'intermediate-region', 'region-code', 'sub-region-code',
       'intermediate-region-code', 'country-code', 'iso_3166-2'], axis=1, inplace=True)
    
    continents.replace({'Americas': 'America'}, inplace=True)
    return continents

#Function 7
def rename_continent_columns():
    """
    Rename columns in continents DataFrame
    """
    continents.rename(columns={'alpha-2': 'country_code',
                        'name': 'country',
                        'region': 'continent'}, inplace=True)
    return continents

#Function 8
def read_room_types(file):
    """
    Reading room types csv file
    """
    rooms = pd.read_csv(f"./data/{file}")
    return rooms

#Function 9
def fix_data_reservations(df):
    """
    Locates reservations with '0' nights and fixes them
    after having checked their info in our database
    """
    # Duplicate data or failed data
    df = df[~df['reservation_id'].isin([623, 3765, 5818])]
    # Inhouse reservation (counting one night)
    df.loc[df['reservation_id'] == 2160, 'nights'] = 1
    # Cancelled reservations
    df.loc[df['nights'] == 0, 'status'] = 'Cancelled'
    return df

#Function 10
def create_calendar_table(start_date, end_date):
    """
    It creates a calendar table 
    """
    dates = pd.date_range(start=start_date, end=end_date)
    
    df = pd.DataFrame({'date': dates})
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['weekday'] = df['date'].dt.day_name()
    df['weekday_number'] = df['date'].dt.weekday
    df['month_name'] = df['date'].dt.month_name()
    df['week'] = df['date'].dt.isocalendar().week
    return df


#Function 11
def rename_and_drop_reservations_columns(df):
    """
    Rename room_id column and drop other information which is detailed in 'rooms' table
    """
    df.rename(columns={'room_id':'room_code'}, inplace=True)
    df.drop(['room_type_id', 'room_type_name'], axis=1, inplace=True)
    return df

#Function 12
def statistics_per_day(df):
    total_rooms = 15
    df['arrival'] = pd.to_datetime(df['arrival'])
    df['departure'] = pd.to_datetime(df['departure'])

    df['stay_duration'] = (df['departure'] - df['arrival']).dt.days
    daily_totals = df.groupby(df['arrival'].dt.date)['accommodation_amount'].sum()

    statistics_per_day = pd.DataFrame(index=pd.date_range(start=df['arrival'].min(), end=df['departure'].max(), freq='D'))
    
    for day in statistics_per_day.index:
        statistics_per_day.loc[day, 'occupied_rooms'] = ((day >= df['arrival']) & (day < df['departure']) & (df['status'] == 'CheckedOut')).sum()
        statistics_per_day['occupancy_rate'] = round(statistics_per_day['occupied_rooms'] / total_rooms * 100, 2)
        statistics_per_day['available_rooms'] = 15 - statistics_per_day['occupied_rooms'] 
        statistics_per_day['avg_daily_rate'] = round(daily_totals / statistics_per_day['occupied_rooms'], 2)
        statistics_per_day['avg_daily_rate'] = statistics_per_day['avg_daily_rate'].replace([np.inf, -np.inf], np.nan).fillna(0)
        statistics_per_day['RevPAR'] = round(daily_totals / statistics_per_day['available_rooms'], 2)
        statistics_per_day['RevPAR'] = statistics_per_day['RevPAR'].replace([np.inf, -np.inf], np.nan).fillna(0)

    cancellations = pd.DataFrame(index=pd.date_range(start=df['arrival'].min(), end=df['departure'].max(), freq='D'))
    for day in cancellations.index:
        bookings_on_day = ((day >= df['arrival']) & (day < df['departure'])).sum()
        if bookings_on_day > 0:
            cancellations_on_day = ((day >= df['arrival']) & (day < df['departure']) & (df['status'] == 'Cancelled')).sum()
            cancellations.loc[day, 'cancelled_bookings'] = cancellations_on_day
            cancellations.loc[day, 'cancellation_percentage'] = round(cancellations_on_day / bookings_on_day * 100, 2)
            
    statistics_per_day = statistics_per_day.merge(cancellations, left_index=True, right_index=True)
    statistics_per_day['year'] = statistics_per_day.index.year
    statistics_per_day['month'] = statistics_per_day.index.month

    return statistics_per_day

#Function 13
def summarize_amount_year(df, occupancy):
    
    # Convert "arrival" column to a datetime type
    df['arrival'] = pd.to_datetime(df['arrival'])
    
    # Create new columns for year
    sales_year = pd.DataFrame(index=pd.date_range(start=df['arrival'].min(), end=df['departure'].max(), freq='Y'))
    for year in sales_year.index:
        sales_year.loc[year, 'year'] = year.year
        sales_year.loc[year, 'total_amount_year'] = df[df['arrival'].dt.year == year.year]['total_amount'].sum()
        sales_year.loc[year, 'board_amount_year'] = df[df['arrival'].dt.year == year.year]['board_amount'].sum()
        sales_year.loc[year, 'service_amount_year'] = df[df['arrival'].dt.year == year.year]['service_amount'].sum()
        sales_year.loc[year, 'accommodation_amount_year'] = df[df['arrival'].dt.year == year.year]['accommodation_amount'].sum()
        
        occupancy['year'] = pd.to_datetime(occupancy['year'], format='%Y')
        occupancy_year = occupancy[occupancy['year'].dt.year == year.year]
        sales_year.loc[year, 'RevPAR'] = occupancy_year['RevPAR'].mean()
        sales_year.loc[year, 'avg_daily_rate'] = occupancy_year['avg_daily_rate'].mean()

    # Convert "year" column to int
    sales_year['year'] = pd.to_numeric(sales_year['year']).astype('Int64')
    
    return sales_year


#Function 14
def occupancy_table(df):
    df['arrival'] = pd.to_datetime(df['arrival'])
    df['departure'] = pd.to_datetime(df['departure'])
    occupancy_2 = pd.concat([pd.DataFrame({'date': pd.date_range(start=row['arrival'], end=row['departure'], freq='D'),
                                           'reservation_id': row['reservation_id'],
                                           'country_code': row['country_code'],
                                           'status': row['status'],
                                           'board': row['board'],
                                           'room_code': row['room_code'],
                                           'adult': row['adult'],
                                           'booker_name': row['booker_name'], 
                                           'nights': row['nights']}) 
                             for i, row in df.iterrows()], ignore_index=True)
    return occupancy_2



import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, fbeta_score, confusion_matrix
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.svm import SVR
from sklearn import metrics
from sys import platform
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import Ridge, Lasso
from sklearn.linear_model import SGDRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR


#Function 15
def merging_tables(occupancy_df, reservations):
    reservations['arrival'] = pd.to_datetime(reservations['arrival'])
    reservations['departure'] = pd.to_datetime(reservations['departure'])
    
    # Merge reservations dataframe to get amount information
    occupancy_df = occupancy_df.merge(reservations[['reservation_id', 'total_amount', 'service_amount', 'board_amount', 'accommodation_amount', 'nights']], 
                  on='reservation_id', how='left')
    
    # Divide the amount columns by nights to get the amount per night
    occupancy_df['total_amount_per_night'] = occupancy_df['total_amount'] / occupancy_df['nights_x']
    occupancy_df['service_amount_per_night'] = occupancy_df['service_amount'] / occupancy_df['nights_x']
    occupancy_df['board_amount_per_night'] = occupancy_df['board_amount'] / occupancy_df['nights_x']
    occupancy_df['accommodation_amount_per_night'] = occupancy_df['accommodation_amount'] / occupancy_df['nights_x']

    # localize the last row for each reservation and set the last row's amount columns to zero
    last_row = occupancy_df.groupby('reservation_id').tail(1).index
    occupancy_df.loc[last_row, ['total_amount_per_night', 'service_amount_per_night', 'board_amount_per_night', 'accommodation_amount_per_night']] = 0
    
    return occupancy_df

#Function 16
def merging_df_roomcode(df1, df2):
    df1.set_index(['room_code'])
    df2.set_index(['room_code'])
    df = pd.merge(df1, df2, on='room_code', how='outer') 
    return df

#Function 17
def getting_ready_for_predicting(df):
    df.rename(columns={'nights_x':'nights'}, inplace=True)
    df.drop(['total_amount_per_night', 'service_amount_per_night', 'board_amount_per_night', 'room_type_name'], axis=1, inplace=True)
    df['room_code'].replace({'NOT_ASSIGNED': '0'}, inplace=True)
    df['room_type'].replace({'NOT_ASSIGNED': '0'}, inplace=True)
    return df

#Function 18
def label_board(x):
    if 'BB' in x:
        return 1
    elif 'RO' in x:
        return 2

#Function 19
def label_booker_name(x):
    if 'WEBSITE' in x:
        return 1
    elif 'BOOKING' in x:
        return 2
    elif 'OTHER' in x:
        return 3
    elif 'EXPEDIA' in x: 
        return 4
    elif 'HOTELBEDS' in x:
        return 5

#Function 20
def calculate_opening_days(df):
    # Group reservations by date
    reservations_by_date = df.groupby('date')

    # Initialize a dictionary to store whether the hotel was open on each date
    opening_days = {}

    # Iterate over each date and check if at least one reservation had status "CheckedOut"
    for date, reservations in reservations_by_date:
        if (reservations['status'] == 'CheckedOut').any():
            opening_days[date] = 1
        elif (reservations['status'] == 'Cancelled').all():
            opening_days[date] = 0

    # Convert the opening_days dictionary to a DataFrame with a "date" and "opened" column
    opening_days_df = pd.DataFrame.from_dict({'date': list(opening_days.keys()), 'opened': list(opening_days.values())})

    # Merge the opening_days DataFrame with the original DataFrame on the "date" column
    df_with_opening_days = pd.merge(df, opening_days_df, on='date')

    return df_with_opening_days

 
#Function 21
def label_status(x):
    if 'CheckedOut' in x:
        return 1
    elif 'Cancelled' in x:
        return 2
    

#Function 22
def drop_zero_rows(df):
    return df[df['accommodation_amount_per_night'] != 0]













