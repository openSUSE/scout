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

def ins(obj):
    for i in inspect.getmembers(obj): print i

class SolvParser(object):

    etcpath = '/etc/zypp/repos.d'
    solvfile = '/var/cache/zypp/solv/%s/solv'
    binpaths = ( '/bin/', '/sbin/', '/usr/bin/', '/usr/sbin/', '/usr/games/', '/opt/kde3/bin/', '/opt/kde3/sbin/', '/opt/gnome/bin/', '/opt/gnome/sbin/' )

    def __init__(self):
        self.pool = satsolver.Pool()
        self.parser = SafeConfigParser()
        for repofile in filter(lambda x: fnmatch(x, '*.repo'), os.listdir(self.etcpath)):
            try:
                name = os.path.splitext(repofile)[0]
                self.parser.read( '%s/%s' % (self.etcpath, repofile) )
                if self.parser.get(name, 'enabled') == '1':
                    self.pool.add_solv( self.solvfile % name )
                print name, '... added'
            except:
                pass

    def search(self, term): # returns fullpath, package
#         pool = satsolver.Pool()
#         pool.add_solv('/home/prusnak/work/scm/zypp/sat-solver/bindings/python/tests/os11-biarch.solv')
         pool = self.pool
         filematch = map(lambda x: x + term, self.binpaths)
         pkgmatch = []

#         for solv in pool:
#             print solv
#             if solv.attr_exists('solvable:filelist'):
#                 print solv.attr('solvable:filelist')
#             else:
#                 print '-'

         for solv in pool:
             filelist = None
             if solv.attr_exists('solvable:filelist'):
                 filelist = solv.attr('solvable:filelist')
             if not isinstance(filelist, list):
                 filelist = [ filelist ]
             for file in filelist:
                 if file in filematch:
                     pkgmatch.append( ( 'zypp', term, file , solv.name() ) )
                     return pkgmatch

         return pkgmatch

r = SolvParser()
# print r.search('acroread')
print r.search('foobillard')
print r.search('wireshark')
