#!/usr/bin/python

import csv
from pysqlite2 import dbapi2 as sqlite3

conn = sqlite3.connect('vizdata.sqlite3')

# load spatialite
# conn.enable_load_extension(True)
# conn.load_extension('libspatialite.2.dylib')

c = conn.cursor()

c.execute('drop table if exists pols')
c.execute('create table pols (id integer primary key autoincrement not null, name text, ext_id text, party char(1), state text, district text, seat text)')
c.execute('create unique index if not exists pk on pols (id)')

c.execute('drop table if exists contributions')
# c.execute('create table contributions (id integer primary key autoincrement not null, pols_id integer not null, name text, date integer, amount float, address text, city text, state text, zipcode text)')
c.execute('create table contributions (id integer primary key autoincrement not null, pols_id integer not null, name text, date integer, amount float, address text, city text, state text, zipcode text, x float, y float)')
c.execute('create unique index if not exists pk on contributions (id)')
c.execute('create index if not exists pols_fk on contributions(pols_id)')
c.execute('create index if not exists date_index on contributions(date)')

# c.execute("select AddGeometryColumn('contributions', 'coords', 4326, 'POINT', 2)")

pol_ids = c.execute('select distinct recipient_ext_id from orig_data where seat = "federal:house" or seat = "federal:senate" or seat = "federal:president"')

for p in pol_ids.fetchall():
    if p:
        print p
        c.execute('insert into pols (name, ext_id, party, state, district, seat) select recipient_name, recipient_ext_id, recipient_state, recipient_party, district, seat from orig_data where recipient_ext_id = ? limit 1', p)
        pid = c.lastrowid
        print pid
        
        c.execute('insert into contributions(pols_id, name, date, amount, address, city, state, zipcode) select ?, contributor_name, strftime("%s", replace(date, "/", "-") || " 12:00:00"), amount, contributor_address, contributor_city, contributor_state, contributor_zipcode from orig_data where recipient_ext_id = ?', (pid, p[0]))

conn.commit()
