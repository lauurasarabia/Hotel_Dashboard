import pandas as pd
import seaborn as sns
import datetime


#Function 1
def read_concat_csv(file1, file2, file3, file4):
    """
    Read and concat dataframes vertically
    """
    df1 = pd.read_csv(f"/Users/lauurasarabia/ironhack/projects/final_project/data/{file1}")
    df2 = pd.read_csv(f"/Users/lauurasarabia/ironhack/projects/final_project/data/{file2}")
    df3 = pd.read_csv(f"/Users/lauurasarabia/ironhack/projects/final_project/data/{file3}")
    df4 = pd.read_csv(f"/Users/lauurasarabia/ironhack/projects/final_project/data/{file4}")

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

