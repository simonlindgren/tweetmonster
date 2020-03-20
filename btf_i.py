#!/usr/bin/env python3

'''
BACK TO FUTURE TWEET INSPECTOR
'''

import shutil
import sqlite3
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--project", default = "btf")
args = parser.parse_args()

def main():
    print("")
    inspector(args.project)

def inspector(projectname):
    # live inspectory
    shutil.copy(projectname + "_live.db", "templive.db")
    db1 = sqlite3.connect("templive.db")
    db1_cursor = db1.cursor()
    db1_cursor.execute("select created_at from tweets")
    db1_count = len(db1_cursor.fetchall())
    os.remove("templive.db")
    
    # history inspectore
    shutil.copy(projectname + "_hist.db", "temphist.db")
    db2 = sqlite3.connect("temphist.db")
    db2_cursor = db2.cursor()
    db2_cursor.execute("select created_at from tweets")
    db2_count = len(db2_cursor.fetchall())
    os.remove("temphist.db")
    
    oldest = list(db2_cursor.execute("select created_at from tweets"))[-1]
    oldest = " ".join(oldest)[:-11]
    
    print(projectname)
    print("*"*len(projectname) + "\n")
    print(str(db1_count) + " live streamed tweets")
    print(str(db2_count) + " historical tweets" + "\t\tDataset start is now: " + oldest)
    
if __name__ == '__main__':
    main()