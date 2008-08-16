# Copyright (c) 2008 Pavol Rusnak
# see __init__.py for license details

import scout
import sys

try:
    satsolver = __import__('satsolver')
    import os
    from fnmatch import fnmatch
    from ConfigParser import SafeConfigParser
except:
    satsolver = None

class SolvParser(object):

    etcpath = '/etc/zypp/repos.d'
    solvfile = '/var/cache/zypp/solv/%s/solv'
    cache_file = '/var/cache/scout/zypp.db'
    binpaths = ( '/bin', '/sbin', '/usr/bin', '/usr/sbin', '/usr/games', '/opt/kde3/bin', '/opt/kde3/sbin', '/opt/gnome/bin', '/opt/gnome/sbin' )

    def __init__(self):
        self.refresh_cache()

    def search(self, term):
        self.refresh_cache()

        db = scout.Database( self.cache_file )

        r = db.query('SELECT "zypp (" || repository || ")", binary, path, package FROM binary LEFT JOIN path ON binary.id_path=path.id_path LEFT JOIN package ON binary.id_pkg=package.id_pkg LEFT JOIN repository ON package.id_repo=repository.id_repo WHERE binary=?', term)

        if r == None:
            return None
        if isinstance(r, list):
            return r
        else:
            return [r]

    def refresh_cache(self):
        parser = SafeConfigParser()
        repos = dict()
        max_mtime = 0
        # find repositories in etcpath
        for repofile in filter(lambda x: fnmatch(x, '*.repo'), os.listdir(self.etcpath)):
            try:
                name = os.path.splitext(repofile)[0]
                parser.read( '%s/%s' % (self.etcpath, repofile) )
                if parser.get(name, 'enabled') == '1':
                    repos[name] = len(repos)
                    # find the newest repository
                    mtime = os.stat( self.solvfile % name )[8]
                    if mtime > max_mtime:
                        max_mtime = mtime
            except:
                pass

        try:
            stat = os.stat( self.cache_file )
        except:
            stat = None

        # if cache is not empty (filesize is zero) and newer than the newest repo
        if stat != None and stat[6] > 0 and stat[8] > max_mtime:
            return

        # create cache from satsolver files
        pool = satsolver.Pool()

        f = open( self.cache_file, 'w' )
        f.truncate()
        f.close()
        try:
            os.chmod( self.cache_file, 0666)
        except:
            pass

        db = scout.Database( self.cache_file )
        db.begin()
        db.execute('CREATE TABLE binary(binary VARCHAR(64) NOT NULL, id_path INT NOT NULL, id_pkg INT NOT NULL)')
        db.execute('CREATE TABLE path(id_path INT PRIMARY KEY NOT NULL, path VARCHAR(64) NOT NULL)')
        db.execute('CREATE TABLE package(id_pkg INT PRIMARY KEY NOT NULL, package VARCHAR(64) NOT NULL, id_repo INT NOT NULL)')
        db.execute('CREATE TABLE repository(id_repo INT PRIMARY KEY NOT NULL, repository VARCHAR(64) NOT NULL)')

        paths = dict()
        pkgs = dict()
        entries = dict()

        for reponame in repos.keys():
            repo = pool.add_solv( self.solvfile % reponame )
            db.execute('INSERT INTO repository(id_repo, repository) VALUES(?, ?);', repos[reponame], reponame )
            for solv in repo:
                if not pkgs.has_key(solv.name()):
                    pkgs[ solv.name() ] = len(pkgs)
                    db.execute('INSERT INTO package(id_pkg, package, id_repo) VALUES(?, ?, ?)', pkgs[solv.name()], solv.name(), repos[reponame])
                if not solv.attr_exists('solvable:filelist'):
                    continue
                for file in solv.attr('solvable:filelist'):
                    if entries.has_key(solv.name()+file):
                        continue
                    entries[ solv.name()+file] = True
                    (path, binary) = os.path.split(file)
                    if path in self.binpaths:
                        if not paths.has_key(path):
                            paths[ path ] = len(paths)
                            db.execute('INSERT INTO path(id_path, path) VALUES(?, ?)', paths[path], path )
                        db.execute('INSERT INTO binary(binary, id_path, id_pkg) VALUES(?, ?, ?)', binary, paths[path], pkgs[solv.name()])

        db.execute('CREATE INDEX binary_bin_idx ON binary(binary)');
        db.end()

class ScoutModule(object):

    name = "bin"
    desc = "Search for binaries contained in the packages."

    @classmethod
    def query_zypp(cls, term):
        if satsolver == None:
            return None
        s = SolvParser()
        return s.search(term)

    @classmethod
    def query_repo(cls, repo, term):
        db = scout.Database(cls.name + '-' + repo)
        r = db.query('SELECT binary, path, package FROM binary LEFT JOIN path ON binary.id_path=path.id_path LEFT JOIN package ON binary.id_pkg=package.id_pkg WHERE binary=?', term)
        if r == None:
            return None
        if isinstance(r, list):
            return map( lambda x: [repo] + list(x), r)
        else:
            return [ [repo] + list(r) ]

    @classmethod
    def main(cls):

        p = scout.Parser(cls.name)
        p.add_repo('zypp')
        if not p.parse():
            return None
        term = p.args[0]

        result = scout.Result( ['repo', 'bin', 'path', 'pkg'], ['repository', 'binary', 'path', 'package']);

        for repo in p.get_repos():
            if repo == 'zypp':
                result.add_rows( cls.query_zypp(term) )
            else:
                result.add_rows( cls.query_repo(repo, term) )

        return result
