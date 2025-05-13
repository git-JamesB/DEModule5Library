import pandas as pd
import os

#Functions
def load_csv(file_name, folder):
    file_path = os.path.join(folder, file_name)
    return pd.read_csv(file_path)

def dateDuration(date1, date2, df):
    df['date_delta'] = (df[date1]-df[date2]).dt.days
    return df.head()

def removeblanks(df, column):
    df = df[df[column].notna()]
    return df

def dupecheck(df):
    dupe_count = df.duplicated().sum()
    if dupe_count > 0:
        df.drop_duplicates()
        return print(f'{dupe_count} duplicates will be removed')
    else:
        return print("No Duplicates")

def todatetime(df, column):
    df[column] = df[column].str.replace('"', '', regex = False)
    df[column] = pd.to_datetime(df[column], dayfirst = True, errors = 'coerce')
    return df
