import pandas as pd
import sqlalchemy as s

#get csv data
df = pd.read_csv('Data/03_Library Systembook.csv')
df_cust = pd.read_csv('Data/03_Library SystemCustomers.csv')

## cleanse book data
# row counts
print("book row count:" + str(df.shape[0]))

# empty cells
empty_rows = df.isna()
print(empty_rows.sum())

# view empty Id's
empty_id = df[df['Id'].isna()]
print(empty_id)
#alter df to exclude blanks IDs
df = df[df['Id'].notna()]

# recheck empty cells
empty_rows = df.isna()
print(empty_rows.sum())

# empty books
empty_books = df[df['Books'].isna()]
empty_books
# alter df to exclude blanks books
df = df[df['Books'].notna()]

#format returned dates
df['Book Returned'] = pd.to_datetime(df['Book Returned'], dayfirst = True, errors = 'coerce')

#format checkout dates
df['Book checkout'] = df['Book checkout'].str.replace('"', '', regex = False)
df['Book checkout'] = pd.to_datetime(df['Book checkout'], dayfirst = True, errors = 'coerce')

#duplicate check
dupe_count = df.duplicated().sum()
if dupe_count > 0:
    print('Duplicates will be removed')
    df.drop_duplicates()
else:
    print("No Duplicates")

# check for non sensical returned dates
invalid = df[df['Book Returned'] < df['Book checkout']]
print(invalid)
#flag invalid
df['ReturnBeforeCheckout'] = df['Book Returned'] < df['Book checkout']



## cleanse customer data
print(df_cust.head(10))
print("Customer row count:" + str(df_cust.shape[0]))

#empty cells
empty_rows = df_cust.isna()
print(empty_rows.sum())

# view empty Id's
empty_id = df_cust[df_cust['Customer ID'].isna()]
print(empty_id)
#alter df to exclude blanks IDs
df_cust = df_cust[df_cust['Customer ID'].notna()]

print("Customer row count:" + str(df_cust.shape[0]))

#duplicate check
dupe_count = df_cust.duplicated().sum()
if dupe_count > 0:
    print('Duplicates will be removed')
    df_cust.drop_duplicates()
else:
    print("No Duplicates")

#missing customer
##need to bring cleaned customers into same script then then customer id in that df


## Insert into SQL
connection_string = 'mssql+pyodbc://@localhost/Library?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
engine = s.create_engine(connection_string)

df_cust.to_sql('Customer', con = engine, if_exists = 'replace', index = False)
df.to_sql('Books', con = engine, if_exists = 'replace', index = False)