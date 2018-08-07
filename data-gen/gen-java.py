#!/usr/bin/python3
import fnmatch
import os


def process(s):
    print('Processing %s ...' % s, end=' ')
    jars = {}
    pkgs = {}
    f = os.popen('lzma -c -d %s.txt.lzma' % s)
    g = open(s+'.sql', 'w')
    g.write('BEGIN;\n')
    g.write('CREATE TABLE classes('
            'class VARCHAR(64) NOT NULL, '
            'id_jar INT NOT NULL);\n')
    g.write('CREATE TABLE jars('
            'id_jar INT PRIMARY KEY NOT NULL, '
            'jar VARCHAR(64) NOT NULL, '
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
        if (line[0]+line[1]) not in jars:
            jars[line[0]+line[1]] = len(jars)
            g.write('INSERT INTO jars(id_jar, jar, id_pkg) '
                    "VALUES(%s, '%s', %s);\n" % (
                        jars[line[0]+line[1]], line[1], pkgs[line[0]]))
        g.write('INSERT INTO classes(class, id_jar) '
                "VALUES('%s', %s);\n" % (line[2], jars[line[0]+line[1]]))
    g.write('CREATE INDEX classes_class_idx ON classes(class);\n')
    g.write('CREATE INDEX jars_jar_idx ON jars(jar);\n')

    g.write('COMMIT;\n')
    f.close()
    g.close()
    print('done')


for file in os.listdir('.'):
    if fnmatch.fnmatch(file, 'java-*.txt.lzma'):
        process(file[:-9])
