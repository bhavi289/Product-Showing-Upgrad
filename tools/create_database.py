import os
import sqlite3
import pandas as pd

data_url = 'https://people.sc.fsu.edu/~jburkardt/data/csv/addresses.csv'
headers = ['product_name','product_price','product_discount', 'product_description']
# AllProducts = pd.read_csv('products.csv', header=None, names=headers, converters={'zip': str})
AllProducts = pd.read_csv('/Users/bhavi/Downloads/slick-crud-app-master/tools/products.csv', header=None, names=headers, converters={'zip': str})


# Clear example.db if it exists
if os.path.exists('example.db'):
    os.remove('example.db')

# Create a database
conn = sqlite3.connect('example.db')

# Add the data to our database
AllProducts.to_sql('AllProducts', conn, dtype={
    'product_name':'VARCHAR(256)',
    'product_price':'VARCHAR(256)',
    'product_discount':'VARCHAR(256)',
    'product_description': 'VARCHAR(2048)'
})

conn.row_factory = sqlite3.Row

# Make a convenience function for running SQL queries
def sql_query(query):
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def sql_edit_insert(query,var):
    cur = conn.cursor()
    cur.execute(query,var)
    conn.commit()

def sql_delete(query,var):
    cur = conn.cursor()
    cur.execute(query,var)

def sql_query2(query,var):
    cur = conn.cursor()
    cur.execute(query,var)
    rows = cur.fetchall()
    return rows
