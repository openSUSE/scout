#!/usr/bin/python
import sys

file = sys.argv[1]
jtab = 'jtab'
cols = sys.argv[2:]

vals = list()
for i in range(0,len(cols)):
    vals.append( dict() )

lines = list()
f = open(file)
for line in f:
    line = line.strip().split('|')
    lines.append( line )
    for i in range(0,len(cols)):
         if not vals[i].has_key(line[i]):
             vals[i][line[i]] = len(vals[i])
f.close()

print 'BEGIN;'
print

for i in range(0,len(cols)):
    print 'CREATE TABLE %s(id INT PRIMARY KEY NOT NULL, str VARCHAR(%s) NOT NULL);' % ( cols[i] , len(max(vals[i].keys(), key=len)) )
    print
    for k in vals[i].keys():
        print "INSERT INTO %s(id, str) VALUES(%s, '%s');" % ( cols[i], vals[i][k], k)
    print
    print 'CREATE INDEX %s_str_idx ON %s(str);' % ( cols[i], cols[i] )
    print

print 'CREATE TABLE %s(' % jtab, ', '.join( map(lambda x: 'id_' + x + ' INT NOT NULL',  cols) ), ');'
print

for line in lines:
    print 'INSERT INTO %s(' % jtab, ', '.join( map(lambda x: 'id_' + x, cols) ), ') VALUES(', ', '.join( map(lambda i,x: str(vals[i][x]), range(0,len(cols)), line) ) , ');'
print
for c in cols:
    print 'CREATE INDEX %s_id_%s_idx ON %s(id_%s);' % (jtab, c, jtab, c)
print

print 'COMMIT;'
