#!/usr/bin/env python3
import fnmatch
import os


def process(s):
    print('Processing %s ...' % s, end=' ')
    m4s = {}
    pkgs = {}
    f = os.popen('lzma -c -d %s.txt.lzma' % s)
    g = open(s+'.sql', 'w')
    g.write('BEGIN;\n')
    g.write('CREATE TABLE macros('
            'macro VARCHAR(64) NOT NULL, '
            'id_m4 INT NOT NULL);\n')
    g.write('CREATE TABLE m4s('
            'id_m4 INT PRIMARY KEY NOT NULL, '
            'm4 VARCHAR(64) NOT NULL, '
            'id_pkg INT NOT NULL);\n')
    g.write('CREATE TABLE packages('
            'id_pkg INT PRIMARY KEY NOT NULL, '
            'package VARCHAR(64) NOT NULL);\n')

    for line in f:
        line = line.strip().split(' ')
        if line[0] not in pkgs:
            pkgs[line[0]] = len(pkgs)
            g.write('INSERT INTO packages(id_pkg, package) '
                    "VALUES(%s, '%s');\n" % (pkgs[line[0]], line[0]))
        if (line[0]+line[1]) not in m4s:
            m4s[line[0]+line[1]] = len(m4s)
            g.write('INSERT INTO m4s(id_m4, m4, id_pkg) '
                    "VALUES(%s, '%s', %s);\n" % (
                        m4s[line[0]+line[1]],
                        line[1], pkgs[line[0]]))
        g.write('INSERT INTO macros(macro, id_m4) '
                "VALUES('%s', %s);\n" % (
                    line[2],
                    m4s[line[0]+line[1]]))
    g.write('CREATE INDEX macros_macro_idx ON macros(macro);\n')
    g.write('CREATE INDEX m4s_m4_idx ON m4s(m4);\n')

    g.write('COMMIT;\n')
    f.close()
    g.close()
    print('done')


for file in os.listdir('.'):
    if fnmatch.fnmatch(file, 'autoconf-*.txt.lzma'):
        process(file[:-9])
