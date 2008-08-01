# Copyright (c) 2008 Pavol Rusnak
# see __init__.py for license details

import scout
import sys

try:
    zypp = __import__('zypp')
except:
    zypp = None

class ZyppParser(object):

    rebuild_cache = False
    paths = ( '/bin', '/sbin', '/usr/bin', '/usr/sbin', '/usr/games', '/opt/kde3/bin', '/opt/kde3/sbin', '/opt/gnome/bin', '/opt/gnome/sbin' )

    @classmethod
    def list(cls):
        z = zypp.ZYppFactory_instance().getZYpp()
        repoManager = zypp.RepoManager()
        repos = repoManager.knownRepositories()

        for repo in repos:
            if not repo.enabled():
                continue
            if cls.rebuild_cache and not repoManager.isCached(repo):
                repoManager.buildCache(repo)
            repoManager.loadFromCache(repo)

        print "Available items: %d" % ( z.pool().size() )
        for item in z.pool():
            print "* %s:%s-%s.%s\t(%s)" % ( item.resolvable().kind(),
                                            item.resolvable().name(),
                                            item.resolvable().edition(),
                                            item.resolvable().arch(),
                                            item.resolvable().repository().info().alias() )

class ScoutModule(object):

    name = "bin"
    desc = "Search for binaries contained in the packages."

    @classmethod
    def query_zypp(cls, term):
        if zypp == None:
            return None
        # TODO: implement
        return None

    @classmethod
    def query_repo(cls, repo, term):
        db = scout.Database(cls.name + '-' + repo)
        r = db.execute('SELECT binary, path, package FROM binary LEFT JOIN path ON binary.id_path=path.id_path LEFT JOIN package ON binary.id_pkg=package.id_pkg WHERE binary=?', term)
        if r == None:
            return None
        if isinstance(r, list):
            return map( lambda x: [repo] + list(x), r)
        else:
            return [ [repo] + list(r) ]
        return r

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
