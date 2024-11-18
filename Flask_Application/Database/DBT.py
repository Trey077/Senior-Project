
##from prettytable import PrettyTable
##myTable = PrettyTable(["idea", "name", "categories", "assigned_to", "status", "created_at","votes", "tags","description"])

##print(myTable)

import pandas as pd
import pickle
from sqlalchemy import create_engine


engine = create_engine('sqlite://', echo=False)

with open('C:/Senior-Project/notebooks/dream_machine.pkl', 'rb') as file:
    df = pickle.load(file)


df.to_sql('dream_machine', con=engine, if_exists='replace', index=False)

import sqlite3

conn = sqlite3.connect('sqlite://')
cur = conn.cursor()
cur.execute('SELECT * FROM dream_machine')
rows = cur.fetchall()

for row in rows:
    print(row)

