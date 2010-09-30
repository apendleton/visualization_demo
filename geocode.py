#!/usr/bin/python

import csv
from pysqlite2 import dbapi2 as sqlite3

from pyproj import Proj

reader = csv.reader(open('zipcodes.csv'))

zips = {}
for row in reader:
    if row and row[1]:
#        zips[row[0]] = 'POINT(%s %s)' % (float(row[1]), float(row[2]))
        zips[row[0]] = (float(row[1]), float(row[2]))

p = Proj(proj='merc', ellps='WGS84')

conn = sqlite3.connect('vizdata.sqlite3')

# load spatialite
#conn.enable_load_extension(True)
#conn.load_extension('libspatialite.2.dylib')

c = conn.cursor()

r = c.execute('select id, zipcode from contributions')

for row in r.fetchall():
    if row[1] in zips:
#        c.execute('update contributions set  = GeomFromText(?, 4326) where id = ?', (zips[row[1]], row[0]))
        new_coords = p(zips[row[1]][1], zips[row[1]][0])
        c.execute('update contributions set x = ?, y = ? where id = ?', list(new_coords) + [row[0]])

conn.commit()
