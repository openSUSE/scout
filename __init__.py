import fnmatch
import os
import sys
import sqlite3
from optparse import OptionParser

class Config(object):
    data_path = '/usr/share/scout'
    data_suffix = '.db'

class CommandLineParser(object):
    """
    This is a command-line parser for core. Just prints help for available
    modules and should return one of them.

    Instance attributes:
        - modules:      a dictionary contains the pairs [module_name, module_reference]
        - prog:         set a program name

    Example:
        parser = CommandLineParser(list_of_available_modules)
        module = parser.parse()

        module.foo()
    """

    @classmethod
    def __init__(cls, modules = None):
        """
        A constructor for CommandLineParser, argument modules should be inicialized
        """
        cls.modules = dict()

        if modules != None:
            _modules = modules
            if not hasattr(modules, "__iter__"):
                _modules = (modules, )

            for m in _modules:
                cls.add_module(m)

        cls.prog = os.path.basename(sys.argv[0])

    @classmethod
    def add_module(cls, module):
        cls.modules[module.ScoutModule.name] = module

    @classmethod
    def _is_help(cls, arg):
        if arg in ("help", "-h", "-help", "--help"):
            return True
        return False

    @classmethod
    def print_usage(cls):
        print
        print "Usage: %s <module> <search_term> [module-options]" % (cls.prog)
        print
        print "available modules:"
        maxlen = len(max(cls.modules.keys(), key=len))
        for k in sorted(cls.modules.keys()):
            module = cls.modules[k]
            print "    %s : %s" % (module.ScoutModule.name.ljust(maxlen), module.ScoutModule.desc)
        print
        sys.exit(1)

    @classmethod
    def module_not_found(cls, name):
        print "Module '%s' not found" % name
        sys.exit(1)

    @classmethod
    def parse(cls):

        if len(sys.argv) == 1 or (len(sys.argv) == 2 and cls._is_help(sys.argv[1])):
            cls.print_usage()

        mname = sys.argv[1]
        if not mname in cls.modules:
            cls.module_not_found(mname)
        del sys.argv[1]
        return cls.modules[mname]

class ModuleLoader(object):
    """
    The basic module loader - it allows to load a module from specified directory(ies)
    """

    modules = list()

    @classmethod
    def import_from(cls, dirs):
        _dirs = dirs
        # make an non-iter item as iter
        if not hasattr(dirs, "__iter__"):
            _dirs = (dirs, )
        for dir in _dirs:
            cls._import(dir)

    @classmethod
    def _import(cls, dir):
        if not os.path.isdir(dir):
            raise AttributeError("%s is not a directory" % dir)
        sys.path.insert(0, dir)
        for file in os.listdir(dir):
            module_name, ext = os.path.splitext(file)
            if ext == '.py' and module_name != '__init__':
                module = __import__(module_name)
                cls.modules.append(module)

class Database(object):

    def __init__(self, dbname):
        dbfile = Config.data_path + '/' + dbname + Config.data_suffix
        try:
            self.conn = sqlite3.connect(dbfile)
        except:
            print "Could not open database file '%s'" % dbfile
            self.conn = None

    def __del__(self):
        if self.conn != None:
            self.conn.close()

    def _clever_query_result(self, c):
        ret = list()
        for row in c:
            if len(row) == 1:           #(2)
                ret.append(row[0])
            else:                       #(3)
                ret.append(row)
        if len(ret) == 1:               #(1)
            return ret[0]
        return ret

    def execute(self, query, *args, **kwargs):
        """
        an abstract database query - but more clever

        query - a query to proceed

        there're two kinds of placeholders (like as original DB/API execute, but in more Pythonic way)
        - question marks (qmark style):
          execute("SELECT ham, spam FROM foo WHERE bar=? and baz=?", bar, baz)
        - named placeholders (named style)
          execute("SELECT ham, spam FROM foo WHERE bar=:bar and baz=:baz", bar='42', baz='42')

        Note: its not possible to combine this two types of placeholders in one call!

        return
        (1) if the length of the result is one, returns one value
        (2) if the column in the result is the only one, returns a list of values
        (3) else returns a list of tuples
        """

        if self.conn == None:
            return None

        # it is not possible to use both a args and a keyword args
        assert(args!=None or kwargs!=None)

        c = self.conn.cursor()
        if args==None and kwargs==None:
            c.execute(query)
        elif args!=None:
            c.execute(query, args)
        else:
            c.execute(query, kwargs)
        ret = self._clever_query_result(c)
        c.close()
        return ret

class Result(object):

    @classmethod
    def __init__(cls, cols1, cols2 = None):
        cls.cols1 = cols1
        if cols2 != None:
            cls.cols2 = cols2
        else:
            cls.cols2 = cols1
        cls.rows = list()

    @classmethod
    def add_row(cls, row):
        if row != None:
            cls.rows.append(list(row))

    @classmethod
    def add_rows(cls, rows):
        if rows != None and isinstance(rows, list):
            for row in rows:
                cls.rows.append(list(row))

    @classmethod
    def gentable(cls):
        col_width = map(len, map(str, cls.cols2))
        for i in range(0,len(cls.cols2)):
          for row in cls.rows:
            if len(str(row[i])) > col_width[i]:
                col_width[i] = len(str(row[i]))
        print ' ' + ' | '.join(map(str.ljust, cls.cols2, col_width))
        print '-' + '-+-'.join(map(lambda c: '-' * c, col_width)) + '-'
        for row in cls.rows:
            print ' ' + ' | '.join(map(str.ljust, map(str, row), col_width))

    @classmethod
    def gencsv(cls):
        print '"' + '";"'.join(map(lambda s: s.replace('"', '""'), cls.cols1)) + '"'
        print '"' + '";"'.join(map(lambda s: s.replace('"', '""'), cls.cols2)) + '"'
        for row in cls.rows:
            print '"' + '";"'.join(map(lambda s: s.replace('"', '""'), row)) + '"'

    @classmethod
    def genxml(cls):
        print '<result>'
        print '  <head>'
        for i in range(0, len(cls.cols1)):
            print '    <%s>%s</%s>' % (cls.cols1[i], cls.cols2[i], cls.cols1[i])
        print '  </head>'
        for row in cls.rows:
          print '  <row>'
          for i in range(0,len(cls.cols1)):
              print '    <%s>%s</%s>' % (cls.cols1[i], row[i], cls.cols1[i])
          print '  </row>'
        print '</result>'


class Parser(object):

    def __init__(self, modulename):
        self.modulename = modulename
        self.parser = OptionParser(usage="Usage: %prog " + modulename + " [options] <search_term>")
        self.parser.add_option('-l', '--listrepos', action="store_true", help="list available repositories", dest="listrepo")
        self.parser.add_option('-r', '--repo', type='choice', help='select repository to search', default=None, choices=[None])

    def add_repo(self, repo):
        opt = self.parser.get_option('-r')
        opt.choices.append(repo)

    def add_repos(self, repos):
        opt = self.parser.get_option('-r')
        for repo in repos:
            opt.choices.append(repo)

    # set repositories according to data files /usr/share/scout/<modulename>-*.db
    def add_repos_from_datadir(self):
        opt = self.parser.get_option('-r')
        for file in os.listdir(Config.data_path):
            if fnmatch.fnmatch(file, self.modulename + '-*' + Config.data_suffix):
                repo = file[len(self.modulename)+1:-len(Config.data_suffix)]
                opt.choices.append(repo)

    def parse(self):
        (self.options, self.args) = self.parser.parse_args()
        if self.options.listrepo:
            print 'Available repositories:'
            reposconf = open(Config.data_path + '/repos.conf')
            repos={}
            for line in reposconf:
                (k,v) = line.split('=')
                repos[k.strip()] = v.strip()
            reposconf.close()
            if len(self.parser.get_option('-r').choices) < 2:
                print '- none -'
                return False
            maxlen = len(max(self.parser.get_option('-r').choices, key=lambda x: x!=None and len(x) or 0))
            for opt in self.parser.get_option('-r').choices:
                if opt == None:
                    continue
                if repos.has_key(opt):
                  print opt.ljust(maxlen), '-', repos[opt]
                else:
                  print opt
            return False
        if len(self.args) == 0:
            self.parser.print_help()
            return False
        return True

    def get_repos(self):
        if self.options.repo:
            return [self.options.repo]
        elif self.parser.get_option('-r'):
            return [x for x in self.parser.get_option('-r').choices if x!=None]
        else:
            return []

class ScoutCore(object):

    @classmethod
    def run(cls):

        ml = ModuleLoader
        sitedir = max(sys.path, key=lambda x: x.endswith('site-packages'))
        ml.import_from(sitedir + "/scout")

        clp = CommandLineParser(ml.modules)
        module = clp.parse()
        result = module.ScoutModule.main()

        prog = os.path.basename(sys.argv[0])

        if result != None:
            if prog == 'scoutcsv':
                result.gencsv()
            elif prog == 'scoutxml':
                result.genxml()
            else:
                result.gentable()
