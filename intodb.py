import pandas as pd
import sqlite3

#load a csv file into a dataframe
df = pd.read_csv("output_search.csv")


#create a connection
def create_connection():
    conn = sqlite3.connect("employees_details.db")
    curr = conn.cursor()
    return conn, curr


#create a table, overwrite it if it exists
def create_table():
    global conn
    global curr
    curr.execute("""DROP TABLE IF EXISTS careem_employees""")
    curr.execute("""CREATE TABLE careem_employees(
    name text,
    title text,
    location text,
    profile text
    )""")


#inserts data into the database
def insert_data(df):
    global conn
    global curr
    df['name'] = df.name.str.title()
    df['location'] = df['location'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    for i in range(0, len(df)):
        name = df.iloc[i]['name'].strip()
        title = df.iloc[i]['title'].strip()
        location = df.iloc[i]['location'].strip()
        profile = df.iloc[i]['profile'].strip()
        curr.execute("""INSERT INTO careem_employees(name,title, location, profile) VALUES (?,?,?,?)""", (name, title, location, profile))
        conn.commit()


def fetch_data():
    global conn
    global curr
    curr.execute("""SELECT * FROM careem_employees""")
    rows = curr.fetchall()
    for row in rows:
        print("--------")
        print(row[0])
        print(row[1])
        print(row[2])
        print(row[3])






conn, curr = create_connection()
create_table()
insert_data(df)
fetch_data()



