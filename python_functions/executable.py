import pandas as pd
import seaborn as sns
import datetime
import math


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
def occupation(df):
    total_rooms = 15
    df['arrival'] = pd.to_datetime(df['arrival'])
    df['departure'] = pd.to_datetime(df['departure'])
    df['stay_duration'] = (df['departure'] - df['arrival']).dt.days
    occupancy = pd.DataFrame(index=pd.date_range(start=df['arrival'].min(), end=df['departure'].max(), freq='D'))
    for day in occupancy.index:
        occupancy.loc[day, 'occupied_rooms'] = ((day >= df['arrival']) & (day < df['departure'])).sum()
        occupancy['occupancy'] = occupancy['occupied_rooms'] / total_rooms
    return occupancy



