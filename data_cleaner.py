import pandas as pd
import os
from sqlalchemy import create_engine
import datetime as dt

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
    

#get csv data
df_book = load_csv('03_Library Systembook.csv', 'Data')
df_cust = load_csv('03_Library SystemCustomers.csv', 'Data')

# get starting row counts
book_starting_count = df_book.shape[0]
customer_starting_count = df_cust.shape[0]



## cleanse book data
print("Cleaning Book data")

# empty cells
print("Empty rows per column:")
empty_rows = df_book.isna()
print(empty_rows.sum())

#alter df to exclude blanks IDs
df_book = removeblanks(df = df_book, column = 'Id')

# empty books
empty_books = df_book[df_book['Books'].isna()]
empty_books
# alter df to exclude blanks books
df_book = removeblanks(df = df_book, column = 'Books')

#format returned dates
df_book['Book Returned'] = pd.to_datetime(df_book['Book Returned'], dayfirst = True, errors = 'coerce')

#format checkout dates
df_book['Book checkout'] = df_book['Book checkout'].str.replace('"', '', regex = False)
df_book['Book checkout'] = pd.to_datetime(df_book['Book checkout'], dayfirst = True, errors = 'coerce')

#duplicate check
dupecheck(df_book)

#derive load duration column
dateDuration(df=df_book, date1='Book Returned', date2='Book checkout')




## cleanse customer data
print("Cleaning customer data")

#empty cells
empty_rows = df_cust.isna()
print("Empty rows per column:" + str(empty_rows.sum()))

#alter df to exclude blanks IDs
df_cust = removeblanks(df = df_cust, column = 'Customer ID')

#duplicate check
dupecheck(df_cust)

#missing customer
##need to bring cleaned customers into same script then then customer id in that df
invalid_customers_df = df_book[~df_book['Customer ID'].isin(df_cust['Customer ID'])]
invalid_customers_df.count()



# Outputing cleaned files
df_cust.to_csv('Data/customers_cleaned.csv')
df_book.to_csv('Data/books_cleaned.csv')



## Insert into SQL
book_finishing_count = df_book.shape[0]
print(f"Starting Book row count: {book_starting_count}. Finishing Book row count: {book_finishing_count}. {book_starting_count - book_finishing_count} rows dropped.")

customer_finishing_count = df_cust.shape[0]
print(f"Starting Customer row count: {customer_starting_count}. Finishing Customer row count: {customer_finishing_count}. {customer_starting_count - customer_finishing_count} rows dropped.")

connection_string = 'mssql+pyodbc://@localhost/Library?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(connection_string)

df_cust.to_sql('Customer', con = engine, if_exists = 'replace', index = False)
df_book.to_sql('Books', con = engine, if_exists = 'replace', index = False)


# DE Metrics to SSMS as a table
df_metrics = pd.DataFrame(columns = ['Entity', 'Metric', 'Value', 'RanOn'], data = [
    ['Books','Rows dropped',book_starting_count - book_finishing_count, dt.datetime.now()],
    ['Customers','Rows dropped',customer_starting_count - customer_finishing_count, dt.datetime.now()]])

#metrics_df = pd.DataFrame([df_metrics])

# Writing to the server
df_metrics.to_sql('DE_Metrics', con = engine, if_exists = 'append', index = False)