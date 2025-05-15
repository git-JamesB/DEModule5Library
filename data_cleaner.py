import pandas as pd
#import os
#from sqlalchemy import create_engine
import datetime as dt
import custom_functions as cf
    
if __name__ == '__main__':
    #get start datetime
    startdatetime = dt.datetime.now()
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

    #format dates
    date_array = ['Book Returned','Book checkout']
    for date in date_array:
            cf.todatetime(df= df_book, column = date)

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
    #cf.log_row_drops(entity_name='Book', start_count=book_starting_count, df_end=df_book)

    customer_finishing_count = df_cust.shape[0]
    print(f"Starting Customer row count: {customer_starting_count}. Finishing Customer row count: {customer_finishing_count}. {customer_starting_count - customer_finishing_count} rows dropped.")
    #cf.log_row_drops(entity_name='Customer', start_count=customer_starting_count, df_end=df_cust)

    # Print results to console for docker demo
    print(df_cust.head(10))
    print(df_book.head(10))

    ## Insert into SQL
    #write Customer to sql
    cf.writetosql(server = 'localhost', database = 'Library', table = 'Customer', df = df_cust, method = 'replace')
    #write Books to sql
    cf.writetosql(server = 'localhost', database = 'Library', table = 'Books', df = df_book, method = 'replace')

    #for testing runtime metric
    #import time
    #time.sleep(1)

    #set end datetime
    enddatetime = dt.datetime.now()
    pipelineruntime = enddatetime - startdatetime
    pipelineruntime = round(pipelineruntime.total_seconds(),1)

    # DE Metrics to SSMS as a table
    df_metrics = pd.DataFrame(columns = ['Entity', 'Metric', 'Value', 'RanOn'], data = [
        ['Books','Rows dropped',book_starting_count - book_finishing_count, startdatetime],
        ['Books','Rows inserted',book_finishing_count, startdatetime],
        ['Customers','Rows dropped',customer_starting_count - customer_finishing_count, startdatetime],
        ['Customers','Rows inserted',customer_finishing_count, startdatetime],
        ['Pipeline', 'Pipeline runtime (sec)', pipelineruntime, startdatetime]])

    #write DE metrics to sql
    cf.writetosql(server = 'localhost', database = 'Library', table = 'DE_Metrics', df = df_metrics, method = 'append')
