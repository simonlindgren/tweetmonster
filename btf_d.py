#!/usr/bin/env python3

'''
BACK TO FUTURE TWITTER DATA EXTRACTOR
'''

from datetime import datetime
import pandas as pd
import shutil
import sqlite3
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--project", default = "tm")
parser.add_argument("--csv", default=False, action="store_true")
args = parser.parse_args()

def main():
    now = datetime.now() # current date and time
    global nowstring
    nowstring = now.strftime("%Y_%m%d_%H%m")  + "UTC"

    merge_databases(nowstring)
    if args.csv is True:
        make_csv()
    
    
def merge_databases(nowstring):
    shutil.copy(args.project + "_live.db", "templive.db")
    shutil.copy(args.project + "_hist.db", "temphist.db")
    
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
    os.rename('templive.db', str(args.project) + "_" + nowstring + ".db")
    os.remove('temphist.db')

def make_csv():
    
    # Read sqlite query results into a pandas DataFrame
    conn = sqlite3.connect(str(args.project) + "_" + nowstring + ".db")
    tweets_df = pd.read_sql_query("SELECT * from tweets", conn)

    tweets_df = tweets_df.replace({'\n': ' '}, regex=True) # remove linebreaks in the dataframe
    tweets_df = tweets_df.replace({'\t': ' '}, regex=True) # remove tabs in the dataframe
    tweets_df = tweets_df.replace({'\r': ' '}, regex=True) # remove carriage return in the dataframe

    tweets_df.to_csv(str(args.project) + "_" + nowstring + ".csv", index = False, encoding='utf-8')

if __name__ == '__main__':
    main()