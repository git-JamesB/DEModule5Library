import pandas as pd
import os
from sqlalchemy import create_engine
import datetime as dt
import custom_functions as cf
    

#get csv data
df_book = cf.load_csv('03_Library Systembook.csv', 'Data')
df_cust = cf.load_csv('03_Library SystemCustomers.csv', 'Data')

# get starting row counts
book_starting_count = df_book.shape[0]
customer_starting_count = df_cust.shape[0]



## cleanse book data
print("-----Cleaning Book data-----")

# empty cells
print("Empty rows per column:")
empty_rows = df_book.isna()
print(empty_rows.sum())

#alter df to exclude blanks IDs
df_book = cf.removeblanks(df = df_book, column = 'Id')

# alter df to exclude blanks books
df_book = cf.removeblanks(df = df_book, column = 'Books')

#format returned dates
cf.todatetime(df = df_book, column = 'Book Returned')

#format checkout dates
cf.todatetime(df = df_book, column = 'Book checkout')

#duplicate check
cf.dupecheck(df_book)

#derive load duration column
cf.dateDuration(df=df_book, date1='Book Returned', date2='Book checkout')




## cleanse customer data
print("-----Cleaning customer data-----")

#empty cells
empty_rows = df_cust.isna()
print("Empty rows per column: \n" + str(empty_rows.sum()))

#alter df to exclude blanks IDs
df_cust = cf.removeblanks(df = df_cust, column = 'Customer ID')

#duplicate check
cf.dupecheck(df_cust)

#missing customer
#merge data frames
df_book = df_book.merge(df_cust, on='Customer ID', how = 'left')
#remove none matches
df_book = df_book[df_book['Customer Name'].notna()]
#drop customer name from book data
df_book = df_book.drop('Customer Name', axis = 1)


# Outputing cleaned files
df_cust.to_csv('Data/customers_cleaned.csv')
df_book.to_csv('Data/books_cleaned.csv')


# Output before and after row counts
print('-----Summary-----')
book_finishing_count = df_book.shape[0]
print(f"Starting Book row count: {book_starting_count}. Finishing Book row count: {book_finishing_count}. {book_starting_count - book_finishing_count} rows dropped.")

customer_finishing_count = df_cust.shape[0]
print(f"Starting Customer row count: {customer_starting_count}. Finishing Customer row count: {customer_finishing_count}. {customer_starting_count - customer_finishing_count} rows dropped.")


## Insert into SQL
connection_string = 'mssql+pyodbc://@localhost/Library?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(connection_string)

df_cust.to_sql('Customer', con = engine, if_exists = 'replace', index = False)
df_book.to_sql('Books', con = engine, if_exists = 'replace', index = False)


# DE Metrics to SSMS as a table
df_metrics = pd.DataFrame(columns = ['Entity', 'Metric', 'Value', 'RanOn'], data = [
    ['Books','Rows dropped',book_starting_count - book_finishing_count, dt.datetime.now()],
    ['Customers','Rows dropped',customer_starting_count - customer_finishing_count, dt.datetime.now()]])

# Writing to the server
df_metrics.to_sql('DE_Metrics', con = engine, if_exists = 'append', index = False)