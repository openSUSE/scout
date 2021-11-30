# Copyright (c) 2008 Pavol Rusnak
# see __init__.py for license details

from configparser import SafeConfigParser
from fnmatch import fnmatch
from subprocess import call
import gettext
import os
import re
import sys

import scout

_ = gettext.gettext


try:
    solv = __import__('solv')
except Exception:
    solv = None


class SolvParser(object):

    etcpath = '/etc/zypp/repos.d'
    solvfile_pattern = '/var/cache/zypp/solv/%s/solv'
    # path regular expression for binary paths
    pathre = r'^/(bin|sbin|usr/bin|usr/sbin|usr/games|opt/kde3/bin' \
        r'|opt/kde3/sbin|opt/gnome/bin|opt/gnome/sbin)/'

    def __init__(self):
        self.pool = solv.Pool()

        zypper_refresh_failed = False
        for repofile in [f for f in os.listdir(self.etcpath)
                         if fnmatch(f, '*.repo')]:
            try:
                parser = SafeConfigParser()
                parser.read('%s/%s' % (self.etcpath, repofile))
                for name in parser.sections():
                    if parser.get(name, 'enabled') == '1':
                        solvfile = self.solvfile_pattern % \
                                   name.replace('/', '_')
                        if not os.path.isfile(solvfile) \
                           and not zypper_refresh_failed:
                            ret = call('zypper refresh')
                            assert ret, 'zypper refresh failed ' \
                                'with exit code: %s' % ret
                        repo = self.pool.add_repo(name)
                        repo.add_solv(solvfile)
            except OSError:
                zypper_refresh_failed = True
            except Exception:
                pass

        if not list(self.pool.repos_iter()):
            print(_('\nWarning: no repos found - make sure your '
                    'repositories are configured.'), file=sys.stderr)
        if zypper_refresh_failed:
            print(_('\nWarning: incomplete repos found but could '
                    'not refresh - try to refresh manually, e.g. '
                    "with 'zypper refresh'."), file=sys.stderr)

    def search(self, term, inversesearch=False):
        pkgmatch = []
        if not inversesearch:
            pathreprg = re.compile(self.pathre + re.escape(term) + '$')
            # SEARCH_STRING without SEARCH_FILES matches basenames
            for d in self.pool.Dataiterator(solv.SOLVABLE_FILELIST,
                                            term,
                                            solv.Dataiterator.SEARCH_STRING):
                path = str(d)
                # do matching for path
                if not pathreprg.match(path):
                    continue
                row = ('zypp (%s)' % d.solvable.repo.name,
                       d.solvable.name,
                       path[:-len(term)-1], term)
                if row not in pkgmatch:
                    pkgmatch.append(row)
        else:
            pathreprg = re.compile(self.pathre + '[^/]+$')
            for d in self.pool.Dataiterator(solv.SOLVABLE_NAME,
                                            term,
                                            solv.Dataiterator.SEARCH_STRING):
                for d2 in self.pool.Dataiterator_solvid(
                        d.solvid, solv.SOLVABLE_FILELIST):
                    path = str(d2)
                    if not pathreprg.match(path):
                        continue
                    binary = os.path.basename(path)
                    row = ('zypp (%s)' % d.solvable.repo.name.decode('utf-8'),
                           d.solvable.name.decode('utf-8'),
                           path[:-len(binary)-1], binary)
                    if row not in pkgmatch:
                        pkgmatch.append(row)
        return pkgmatch


class ScoutModule(scout.BaseScoutModule):

    name = 'bin'
    desc = _('Search for binaries contained in the packages.')

    def __init__(self):
        super(self.__class__, self).__init__()

        if solv is None:
            self._repo_list = scout.RepoList(self._cls.name)
        else:
            self._repo_list = scout.RepoList(self._cls.name, ('zypp', ))
        self._parser = scout.Parser(self._cls.name, self._repo_list.repos)

    def query_zypp(self, term, inversesearch=False):
        if solv is None:
            return None
        s = SolvParser()
        return s.search(term, inversesearch)

    def query_repo(self, repo, term, inversesearch=False):
        db = scout.Database(self._name + '-' + repo)
        if not inversesearch:
            r = db.query(
                'SELECT package, path, binary '
                'FROM binary '
                'LEFT JOIN path ON binary.id_path=path.id_path '
                'LEFT JOIN package ON binary.id_pkg=package.id_pkg '
                'WHERE binary=?', term)
        else:
            r = db.query(
                'SELECT package, path, binary '
                'FROM binary '
                'LEFT JOIN path ON binary.id_path=path.id_path '
                'LEFT JOIN package ON binary.id_pkg=package.id_pkg '
                'WHERE package=?', term)
        if r is None:
            return None
        if isinstance(r, list):
            return [[repo] + list(x) for x in r]
        else:
            return [[repo] + list(r)]

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
        result_list = [_('repo'), _('pkg'), _('path'), _('bin')]
        result_list2 = [_('repository'), _('package'), _('path'),
                        _('binary')]
        scout.default_lang.install()

        result = scout.Result(result_list, result_list2)

        repos = self._repo_list.repos
        if repos is None:
            return None
        if args.repo:
            repos = (args.repo, )
        for repo in repos:
            if repo == 'zypp':
                result.add_rows(self.query_zypp(term, args.inversesearch))
            else:
                result.add_rows(self.query_repo(repo, term,
                                                args.inversesearch))

        return result
