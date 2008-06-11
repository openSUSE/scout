#!/usr/bin/python
import sys

file = sys.argv[1]
table = sys.argv[2]
cols = sys.argv[3:]

lines=list()
f = open(file)
for line in f:
    line = line.strip().split('|')
    lines.append( line )
f.close()

print 'BEGIN;'
print
print 'CREATE TABLE %s(' % table, ', '.join(map(lambda x: x+' VARCHAR(64) NOT NULL', cols)), ');'
print

for line in lines:
    print 'INSERT INTO %s(' %table, ', '.join(cols), ") VALUES(", ", ".join(map(lambda x: "'%s'"%x, line)), ");"
print

c = cols[0]
print 'CREATE INDEX %s_%s_idx ON %s(%s);' % (table, c, table, c)
print

print 'COMMIT;'
