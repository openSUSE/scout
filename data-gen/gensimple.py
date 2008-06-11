#!/usr/bin/python
import sys

file = sys.argv[1]
table = 'tab'
cols = sys.argv[2:]

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

for c in cols:
    print 'CREATE INDEX %s_idx ON %s(%s);' % (c, table, c)
print

print 'COMMIT;'
