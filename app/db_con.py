import psycopg2

DB_HOST = 'localhost'
DB_USERNAME = 'muchogo'
DB_PASS='Muchogo2018'
DB_NAME='politico'
DB_PORT='5432'

URL = "dbname='{}' host='{}' port='{}' user='{}' \
 password='{}'".format(DB_NAME,DB_HOST,DB_PORT,DB_USERNAME,DB_PASS)

# table1 = 
# table2 = 
# table_queries = [table1,table2]

def connection(url):
    conn = psycopg2.connect(URL)
    return conn

def create_tables(query):
    conn = connection(URL)
    curr = conn.cursor()
    for i in query:
        curr.execute(i)
    conn.commit()

def db_migrate():
    create_tables(table_queries)