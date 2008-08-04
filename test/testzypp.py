#!/usr/bin/python
import os
import sys
from fnmatch import fnmatch
from ConfigParser import SafeConfigParser

import inspect

try:
    satsolver = __import__('satsolver')
except:
    satsolver = None

class SolvParser(object):

    etcpath = '/etc/zypp/repos.d'
    solvfile = '/var/cache/zypp/solv/%s/solv'
    paths = ( '/bin', '/sbin', '/usr/bin', '/usr/sbin', '/usr/games', '/opt/kde3/bin', '/opt/kde3/sbin', '/opt/gnome/bin', '/opt/gnome/sbin' )

    def __init__(self):
        self.pool = satsolver.Pool()
        self.parser = SafeConfigParser()
        for repofile in filter(lambda x: fnmatch(x, '*.repo'), os.listdir(self.etcpath)):
            try:
                name = os.path.splitext(repofile)[0]
                self.parser.read( '%s/%s' % (self.etcpath, repofile) )
                if self.parser.get(name, 'enabled') == '1':
                    self.pool.add_solv( self.solvfile % name )
            except:
                pass

    def search(self, term): # returns fullpath, package
        for i in range(self.pool.size()):
            print self.pool.get(i).set_vendor('filelist')
            for xxx in inspect.getmembers(self.pool.get(i)): print xxx
            sys.exit(2)
            prov = self.pool.get(i).provides()
            for j in range(prov.size()):
                rel = prov.get(j+1).to_s()
                print rel

r = SolvParser()
print r.search('wireshark')
