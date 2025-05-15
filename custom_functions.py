import pandas as pd
import os
from sqlalchemy import create_engine

#Functions
def load_csv(file_name, folder):
    file_path = os.path.join(folder, file_name)
    return pd.read_csv(file_path)

def dateDuration(date1, date2, df):
    #creates column which date diff between two columns
    df['date_delta'] = (df[date1]-df[date2]).dt.days
    return df

def removeblanks(df, column):
    #remove blank rows based on column
    df = df[df[column].notna()]
    return df

def dupecheck(df):
    #count duplicates
    dupe_count = df.duplicated().sum()
    #drop duplicates
    return df.drop_duplicates() #, print(f'{dupe_count} duplicates will be removed')

def todatetime(df, column):
    try:
        #remove quotations
        df[column] = df[column].str.replace('"', '', regex = False)
        #convert to datetime
        df[column] = pd.to_datetime(df[column], dayfirst = True, errors = 'coerce')
        return df
    except Exception as e:
        print(f'Error occured: {e}')

def writetosql(server, database, table, df, method):
    #create connection
    connection_string = f'mssql+pyodbc://@{server}/{database}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
    engine = create_engine(connection_string)
    #write to sql
    try:
        # Write the DataFrame to SQL Server
        df.to_sql(table, con = engine, if_exists = method, index = False)
        print(f"Written to SQL table {table}")
    except Exception as e:
        print(f"Error writing to the SQL Server: {e}")

def log_row_drops(entity_name, start_count, df_end):
    end_count = df_end.shape[0]
    dropped = start_count - end_count
    return print(f"Starting {entity_name} row count: {start_count}. Finishing {entity_name} row count: {end_count}. {dropped} rows dropped.")
