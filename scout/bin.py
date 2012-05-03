# Copyright (c) 2008 Pavol Rusnak
# see __init__.py for license details

import scout
import sys
import os
import re
from fnmatch import fnmatch
from ConfigParser import SafeConfigParser

try:
    satsolver = __import__('satsolver')
except:
    satsolver = None

class SolvParser(object):

    etcpath  = '/etc/zypp/repos.d'
    solvfile = '/var/cache/zypp/solv/%s/solv'
    # path regular expression for binary paths
    pathre   = '^/(bin|sbin|usr/bin|usr/sbin|usr/games|opt/kde3/bin|opt/kde3/sbin|opt/gnome/bin|opt/gnome/sbin)/'

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

    def search(self, term, inversesearch = False):
        pkgmatch = []
        if not inversesearch:
            pathreprg = re.compile(self.pathre + re.escape(term) + '$')
            for d in self.pool.search( term, satsolver.SEARCH_STRING, None, 'solvable:filelist' ):
                path = d.value()
                # do matching for path
                if not pathreprg.match(path): continue
                row = ( 'zypp (%s)' % d.solvable().repo().name().decode('utf-8'), d.solvable().name().decode('utf-8'), path[:-len(term)-1], term )
                if not row in pkgmatch:
                    pkgmatch.append( row )
        else:
            pathreprg = re.compile(self.pathre + '[^/]+$')
            for d in self.pool.search( term, satsolver.SEARCH_STRING, None, 'solvable:name' ):
                for path in d.solvable().attr_values('solvable:filelist'):
                    if not pathreprg.match(path): continue
                    binary = os.path.basename(path)
                    row = ( 'zypp (%s)' % d.solvable().repo().name().decode('utf-8'), d.solvable().name().decode('utf-8'), path[:-len(binary)-1], binary )
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

    def query_zypp(self, term, inversesearch = False):
        if satsolver == None:
            return None
        s = SolvParser()
        return s.search(term, inversesearch)

    def query_repo(self, repo, term, inversesearch = False):
        db = scout.Database(self._name + '-' + repo)
        if not inversesearch:
            r = db.query('SELECT package, path, binary FROM binary LEFT JOIN path ON binary.id_path=path.id_path LEFT JOIN package ON binary.id_pkg=package.id_pkg WHERE binary=?', term)
        else:
            r = db.query('SELECT package, path, binary FROM binary LEFT JOIN path ON binary.id_path=path.id_path LEFT JOIN package ON binary.id_pkg=package.id_pkg WHERE package=?', term)
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
        result_list  = [_("repo"), _("pkg"), _("path"), _("bin")]
        result_list2 = [_("repository"), _("package"), _("path"), _("binary")]
        scout.default_lang.install()

        result = scout.Result( result_list, result_list2 )

        repos = self._repo_list.repos
        if repos == None:
            return None
        if args.repo:
            repos = (args.repo, )
        for repo in repos:
            if repo == 'zypp':
                result.add_rows( self.query_zypp(term, args.inversesearch) )
            else:
                result.add_rows( self.query_repo(repo, term, args.inversesearch) )

        return result
