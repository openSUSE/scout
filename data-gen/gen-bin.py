#!/usr/bin/python
import sys
import os
import fnmatch

def process(s):
    print 'Processing %s ...' % s,
    paths = dict()
    pkgs = dict()
    f = open(s + '.txt')
    g = open(s + '.sql', 'w')
    g.write('BEGIN;\n')
    g.write('CREATE TABLE binary(binary VARCHAR(64) NOT NULL, id_path INT NOT NULL, id_pkg INT NOT NULL);\n')
    for line in f:
        line = line.strip().split('|')
        if not paths.has_key( line[1] ):
            paths[ line[1] ] = len(paths)
        if not pkgs.has_key( line[2] ):
            pkgs[ line[2] ] = len(pkgs)
        g.write("INSERT INTO binary(binary, id_path, id_pkg) VALUES('%s', %s, %s);\n" % (line[0], paths[line[1]], pkgs[line[2]]))
    g.write('CREATE INDEX binary_bin_idx ON binary(binary);\n')

    g.write('CREATE TABLE path(id_path INT PRIMARY KEY NOT NULL, path VARCHAR(64) NOT NULL);\n')
    for k in paths.keys():
        g.write("INSERT INTO path(id_path,path) VALUES(%s, '%s');\n" % (paths[k], k))

    g.write('CREATE TABLE package(id_pkg INT PRIMARY KEY NOT NULL, package VARCHAR(64) NOT NULL);\n')
    for k in pkgs.keys():
        g.write("INSERT INTO package(id_pkg,package) VALUES(%s, '%s');\n" % (pkgs[k], k))

    g.write('COMMIT;\n')
    f.close()
    g.close()
    print 'done'

for file in os.listdir('.'):
    if fnmatch.fnmatch(file, 'bin-*.txt'):
        process(file[:-4])
