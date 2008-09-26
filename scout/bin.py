# Copyright (c) 2008 Pavol Rusnak
# see __init__.py for license details

import scout
import sys
import os
from fnmatch import fnmatch
from ConfigParser import SafeConfigParser

try:
    satsolver = __import__('satsolver')
except:
    satsolver = None

class SolvParser(object):

    etcpath  = '/etc/zypp/repos.d'
    solvfile = '/var/cache/zypp/solv/%s/solv'
    # path regular expression for { /bin, /sbin, /usr/bin, /usr/sbin, /usr/games, /opt/kde3/bin, /opt/kde3/sbin, /opt/gnome/bin, /opt/gnome/sbin }
    pathre   = '^/(s?bin|usr/(s?bin|games)|opt/(kde3|gnome)/s?bin)/%s$'

    def __init__(self):
        self.pool = satsolver.Pool()
        self.parser = SafeConfigParser()

        for repofile in [ f for f in os.listdir(self.etcpath) if fnmatch(f, '*.repo') ]:
            try:
                name = os.path.splitext(repofile)[0]
                self.parser.read( '%s/%s' % (self.etcpath, repofile) )
                if self.parser.get(name, 'enabled') == '1':
                    repo = self.pool.add_solv( self.solvfile % name )
                    repo.set_name(name)
            except:
                pass

    def search(self, term):
        pkgmatch = []
        for repo in self.pool.repos():
            for d in repo.search( self.pathre % term, satsolver.SEARCH_REGEX | satsolver.SEARCH_FILES, None, 'solvable:filelist' ):
                path = d.value()
                row = ( 'zypp (%s)' % repo.name(), term, path[:-len(term)-1] , d.solvable().name() )
                if not row in pkgmatch:
                    pkgmatch.append( row )
        return pkgmatch

class ScoutModule(scout.BaseScoutModule):

    name = "bin"
    desc = _("Search for binaries contained in the packages.")

    def __init__(self):
        super(self.__class__, self).__init__()

        if satsolver == None:
            self._repo_list = scout.RepoList(self._cls.name)
        else:
            self._repo_list = scout.RepoList(self._cls.name, ('zypp', ))
        self._parser    = scout.Parser(self._cls.name, self._repo_list.repos)

    def query_zypp(self, term):
        if satsolver == None:
            return None
        s = SolvParser()
        return s.search(term)

    def query_repo(self, repo, term):
        db = scout.Database(self._name + '-' + repo)
        r = db.query('SELECT binary, path, package FROM binary LEFT JOIN path ON binary.id_path=path.id_path LEFT JOIN package ON binary.id_pkg=package.id_pkg WHERE binary=?', term)
        if r == None:
            return None
        if isinstance(r, list):
            return [ [repo] + list(x) for x in r]
        else:
            return [ [repo] + list(r) ]

    def main(self, module_args=None):

        args = None
        try:
            args = self._parser.parse_args(module_args)
        except scout.HelpOptionFound:
            self._parser.print_help()
            sys.exit(1)

        if args.listrepo:
            return self.do_repo_list()

        term = args.query

        scout.null_lang.install()
        result_list  = [_("repo"), _("bin"), _("path"), _("pkg")]
        result_list2 = [_("repository"), _("binary"), _("path"), _("package")]
        scout.default_lang.install()

        result = scout.Result( result_list, result_list2 )

        repos = self._repo_list.repos
        if repos == None:
            return None
        for repo in repos:
            if repo == 'zypp':
                result.add_rows( self.query_zypp(term) )
            else:
                result.add_rows( self.query_repo(repo, term) )

        return result
