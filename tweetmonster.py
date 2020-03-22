#!/usr/bin/env python3

import os
import sqlite3
import shutil
from datetime import datetime


def make_databases(projectname):
    
    # Create first database and table

    conn = sqlite3.connect(str(projectname) + "_live.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE tweets (
    id TEXT,
    created_at TEXT,
    author TEXT,
    author_location TEXT,
    author_followers INT,
    author_friends INT,
    hashtags TEXT,
    tweet TEXT,
    in_reply_to TEXT,
    lang TEXT,
    method TEXT,
    UNIQUE(id))
    """)
    conn.close()

    print("First database created.")

    # Create second database and table

    conn = sqlite3.connect(str(projectname) + "_hist.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE tweets (
    id TEXT,
    created_at TEXT,
    author TEXT,
    author_location TEXT,
    author_followers INT,
    author_friends INT,
    hashtags TEXT,
    tweet TEXT,
    in_reply_to TEXT,
    lang TEXT,
    method TEXT,
    UNIQUE(id))
    """)
    conn.close()

    print("Second database created.")

    
def extract_data(projectname):
    now = datetime.now() # current date and tim
    nowstring = now.strftime("%Y_%m%d_%H%m")  + "UTC"
    

    shutil.copy(projectname + "_live.db", "templive.db")
    shutil.copy(projectname + "_hist.db", "temphist.db")
    
    db_a = sqlite3.connect('templive.db')
    db_b = sqlite3.connect('temphist.db')
    
    # Get the contents of the first table
    b_cursor = db_b.cursor()
    b_cursor.execute('select * from tweets')
    output = b_cursor.fetchall()   # Returns the results as a list

    # Insert those contents into the second table
    a_cursor = db_a.cursor()
    for row in output:
        try:
            a_cursor.execute('INSERT INTO tweets VALUES (?,?,?,?,?,?,?,?,?,?,?)', row)
        except sqlite3.IntegrityError: # skip duplicate tweet ids
            pass

    # Cleanup
    db_a.commit()
    a_cursor.close()
    b_cursor.close()

    # Rename the merged db, and delete the other
    os.rename('templive.db', projectname + "_" + nowstring + ".db")
    os.remove('temphist.db')
    
    # Read sqlite query results into a pandas DataFrame
    conn = sqlite3.connect(projectname + "_" + nowstring + ".db")
    tweets_df = pd.read_sql_query("SELECT * from tweets", conn)

    tweets_df = tweets_df.replace({'\n': ' '}, regex=True) # remove linebreaks in the dataframe
    tweets_df = tweets_df.replace({'\t': ' '}, regex=True) # remove tabs in the dataframe
    tweets_df = tweets_df.replace({'\r': ' '}, regex=True) # remove carriage return in the dataframe

    tweets_df.to_csv(str(args.project) + "_" + nowstring + ".csv", index = False, encoding='utf-8')

def dbkill():
    if input("This will delete ALL database files in this directory. Continue? (y/n)") != "y":
        exit()

    files = os.listdir()

    for item in files:
        if item.endswith(".db"):
            os.remove(item)
    print("Removed!")
    
    
