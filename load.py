#!/usr/bin/python

import csv, sqlite3

reader = csv.reader(open('contributions.fec.2010.csv'))

conn = sqlite3.connect('vizdata.sqlite3')

first_row = reader.next()
conn.execute('drop table if exists orig_data')
conn.execute('create table orig_data (' + ", ".join(first_row) + ')')

query = 'insert into orig_data values(' + ','.join(['?'] * 39) + ')'
for row in reader:
    conn.execute(query, row)

conn.commit()
conn.execute('create index if not exists recipient_ext_id_index on orig_data (recipient_ext_id)')
conn.commit()
