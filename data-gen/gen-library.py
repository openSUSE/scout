#!/usr/bin/env python3
import fnmatch
import os


def process(s):
    print('Processing %s ...' % s, end=' ')
    libs = {}
    pkgs = {}
    f = os.popen('lzma -c -d %s.txt.lzma' % s)
    g = open(s+'.sql', 'w')

    g.write('''
    BEGIN;
    CREATE TABLE libraries (id_lib INT PRIMARY KEY NOT NULL, library VARCHAR(64) NOT NULL, id_pkg INT NOT NULL);
    CREATE TABLE packages(id_pkg INT PRIMARY KEY NOT NULL, package VARCHAR(64) NOT NULL);
    ''')

    for line in f:
        line = line.strip().split(' ')
        if line[0] not in pkgs:
            pkgs[line[0]] = len(pkgs)
            g.write('INSERT INTO packages(id_pkg, package) '
                    "VALUES(%s, '%s');\n" % (pkgs[line[0]], line[0]))
        if (line[0]+line[1]) not in libs:
            libs[line[0]+line[1]] = len(libs)
            g.write('INSERT INTO libraries(id_lib, library, id_pkg) '
                    "VALUES(%s, '%s', %s);\n" % (
                        libs[line[0]+line[1]], line[1], pkgs[line[0]]))
    g.write('CREATE INDEX libraries_library_idx ON libraries(library);\n')

    g.write('COMMIT;\n')
    f.close()
    g.close()
    print('done')


for file in os.listdir('.'):
    if fnmatch.fnmatch(file, 'library-*.txt.lzma'):
        process(file[:-9])
