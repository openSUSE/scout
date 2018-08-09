#!/usr/bin/python3
import fnmatch
import os


def process(s):
    print('Processing %s ...' % s, end=' ')
    jars = {}
    pkgs = {}
    f = os.popen('lzma -c -d %s.txt.lzma' % s)
    g = open(s+'.sql', 'w')

    g.write('''
    BEGIN;
    CREATE TABLE modules (id_modules INT PRIMARY KEY NOT NULL, module VARCHAR(64) NOT NULL, id_pkg INT NOT NULL);
    CREATE TABLE packages(id_pkg INT PRIMARY KEY NOT NULL, package VARCHAR(64) NOT NULL);
    ''')

    for line in f:
        line = line.strip().split(' ')
        if line[0] not in pkgs:
            pkgs[line[0]] = len(pkgs)
            g.write('INSERT INTO packages(id_pkg, package) '
                    "VALUES(?, '?');\n", pkgs[line[0]], line[0])
        if (line[0]+line[1]) not in jars:
            jars[line[0]+line[1]] = len(jars)
            g.write('INSERT INTO modules(id_modules, module, id_pkg) '
                    "VALUES(?, '?', ?);\n",
                    jars[line[0]+line[1]], line[1], pkgs[line[0]])
    g.write('CREATE INDEX modules_module_idx ON modules(module);\n')

    g.write('COMMIT;\n')
    f.close()
    g.close()
    print('done')


for file in os.listdir('.'):
    if fnmatch.fnmatch(file, 'python-*.txt.lzma'):
        process(file[:-9])
