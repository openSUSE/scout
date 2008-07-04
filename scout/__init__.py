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

    def __init__(self, modules = None):
        """
        A constructor for CommandLineParser, argument modules should be inicialized
        """
        self.modules = dict()

        if modules != None:
            _modules = modules
            if not hasattr(modules, "__iter__"):
                _modules = (modules, )

            for m in _modules:
                self.add_module(m)

        self.__format = 'table'
        
        self.prog = os.path.basename(sys.argv[0])

    def add_module(self, module):
        self.modules[module.ScoutModule.name] = module

    def _is_help(self, arg):
        if arg in ("help", "-h", "-help", "--help"):
            return True
        return False

    def print_usage(self):
        print
        print "Usage: %s <module> <search_term> [module-options]" % (self.prog)
        print
        print "Options:"
        print "  -f FORMAT, --format=FORMAT\tselect the output format (default table)"
        print
        print "available modules:"
        maxlen = len(max(self.modules.keys(), key=len))
        for k in sorted(self.modules.keys()):
            module = self.modules[k]
            print "    %s : %s" % (module.ScoutModule.name.ljust(maxlen), module.ScoutModule.desc)
        print
        sys.exit(1)

    def module_not_found(self, name):
        print "Module '%s' not found" % name
        sys.exit(1)

    def parse_option(self, short_opt, long_opt, default=None):
        opt = default
        if short_opt in sys.argv or long_opt in sys.argv:
            opt_index = sys.argv.index(long_opt) if long_opt in sys.argv else sys.argv.index(short_opt)

            opt = sys.argv[opt_index]
            if opt[:2] == '--' and '=' in opt:
                _opt = s.split('=')[1]
                sys.argv.remove(opt)
                opt = _opt
            else:
                _opt = sys.argv[opt_index + 1]
                sys.argv.remove(opt)
                sys.argv.remove(_opt)
                opt = _opt
        return opt

    def parse(self):

        if len(sys.argv) == 1 or (len(sys.argv) == 2 and self._is_help(sys.argv[1])):
            self.print_usage()

        self.__format = self.parse_option('-f', '--format', 'table')

        mname = sys.argv[1]
        if not mname in self.modules:
            self.module_not_found(mname)
        del sys.argv[1]
        return self.modules[mname]

    def _get_format(self):
        return self.__format

    format = property(_get_format)

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
        if dbname == ':memory:':
            dbfile = dbname
        else:
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
        # TODO: do not return an sqlite3 Errors

        if self.conn == None:
            return None

        # it is not possible to use both a args and a keyword args
        assert(len(args) == 0 or len(kwargs) == 0)

        c = self.conn.cursor()
        if len(args) == 0 and len(kwargs) == 0:
            c.execute(query)
        elif len(args) != 0:
            c.execute(query, args)
        else:
            c.execute(query, kwargs)
        ret = self._clever_query_result(c)
        c.close()
        return ret

class TableFormatter(object):

    @classmethod
    def format(cls, result, vertical_delimiter=' | ', node_delimiter='-+-', horizontal_delimiter='-'):
        """
        This method produces an output as a table. It's a base style of output and is recomended for a commandline use.

        The TableFormatter.format method has three optional arguments to improve the output:
        vertical_delimiter   - the delimiter between rows of the table, default  ' | '
        node_delimiter       - the delimiter between nodes of the table, default '-+-'
        horizontal_delimiter - the delimiter between head of the table and a body, default '-'

        The defult output is
         repository | package                   | jar           | class
        ------------+---------------------------+---------------+--------------------------------
         suse110    | geronimo                  | log4j-1.2.8   | org.apache.log4j.xml.XMLLayout
        """
        #FIXME: this code probably doesn't work with a variable length of the delimiters!
        ret = ""
        col_width = map(len, map(str, result.get_long_names()))
        for i in range(0,len(result.get_long_names())):
          for row in result.get_rows():
            if len(str(row[i])) > col_width[i]:
                col_width[i] = len(str(row[i]))
        ret += ' ' + vertical_delimiter.join(map(str.ljust, result.get_long_names(), col_width)) + '\n'
        ret += horizontal_delimiter + node_delimiter.join(map(lambda c: horizontal_delimiter * c, col_width)) + horizontal_delimiter + '\n'
        for row in result.get_rows():
            ret += ' ' + vertical_delimiter.join(map(str.ljust, map(str, row), col_width)) + '\n'
        return ret

class CSVFormatter(object):

    @classmethod
    def format(cls, result, record_delimiter=';', quote_mark='"'):
        """
        This method produces an output in a CSV format. This style is recomended for the scripting use.

        The CSVFormatter.format method has two optional arguments to improve the output:
        record_delimiter       - the delimiter between records, default ';'
        quote_mark             - the quote used for the records, if the quote mark is in the records, is duplicated, default '"'

        The defult output is
        "repo";"pkg";"jar";"class"
        "repository";"package";"jar";"class"
        "suse110";"geronimo";"log4j-1.2.8";"org.apache.log4j.xml.XMLLayout"
        """
        record_delimiter = quote_mark + record_delimiter + quote_mark
        ret = ""
        ret += quote_mark + record_delimiter.join(map(lambda s: s.replace(quote_mark, 2*quote_mark), result.get_short_names())) + quote_mark + '\n'
        ret += quote_mark + record_delimiter.join(map(lambda s: s.replace(quote_mark, 2*quote_mark), result.get_long_names())) + quote_mark + '\n'
        for row in result.rows:
            ret += quote_mark + record_delimiter.join(map(lambda s: s.replace(quote_mark, 2*quote_mark), row)) + quote_mark + '\n'
        return ret

class XMLFormatter(object):

    @classmethod
    def format(cls, result, result_tag='result', head_tag='head', row_tag='row'):
        """
        This method produces an output in a XML format. This style is recomended for the communication between scout and a external systems.

        The XMLFormatter.format method has three optional arguments to improve the output:
        result_tag      - the name of the tag result, default 'result'
        head_tag        - the name of the tag head, default 'head'
        row_tag         - the name of the tag row, default 'row'

        The defult output is
        <result>
            <head>
                <repo>repository</repo>
                <pkg>package</pkg>
                <jar>jar</jar>
                <class>class</class>
            </head>
            <row>
                <repo>suse110</repo>
                <pkg>geronimo</pkg>
                <jar>log4j-1.2.8</jar>
                <class>org.apache.log4j.xml.XMLLayout</class>
            </row>
        </result>
        """
        ret  = '<%s>' % result_tag + '\n'
        ret += '  <%s>' % head_tag + '\n'
        for i in range(0, len(result.get_short_names())):
            ret += '    <%s>%s</%s>' % (result.get_short_names()[i], result.get_long_names()[i], result.get_short_names()[i]) + '\n'
        ret += '  </%s>' % head_tag + '\n'
        for row in result.rows:
          ret += '  <%s>' % row_tag + '\n'
          for i in range(0,len(result.get_short_names())):
              ret += '    <%s>%s</%s>' % (result.get_short_names()[i], row[i], result.get_short_names()[i]) + '\n'
          ret += '  </%s>' % row_tag + '\n'
        ret += '</%s>' % result_tag + '\n'
        return ret


class Result(object):

    def __init__(self, cols1, cols2 = None):
        self.cols1 = cols1
        if cols2 != None:
            self.cols2 = cols2
        else:
            self.cols2 = cols1
        self.rows = list()

    def add_row(self, row):
        if row != None:
            self.rows.append(list(row))

    def add_rows(self, rows):
        if rows != None and isinstance(rows, list):
            for row in rows:
                self.rows.append(list(row))

    def get_short_names(self):
        return self.cols1

    def get_long_names(self):
        return self.cols2

    def get_table(self):
        ret = [self.cols1, self.cols2]
        ret.extend(self.rows)           # I hate the methods, which returns None!!!
        return ret

    def get_rows(self):
        return self.rows

    def format(self, formatter=TableFormatter, **kwargs):
        return formatter.format(self, **kwargs)

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


    out_formatters = {
            'csv' :     CSVFormatter,
            'xml' :     XMLFormatter,
            'table' :   TableFormatter,
            }

    @classmethod
    def run(cls):

        ml = ModuleLoader
        moduledir = os.path.dirname(__file__)
        ml.import_from(moduledir)

        clp = CommandLineParser(ml.modules)
        module = clp.parse()
        result = module.ScoutModule.main()

        prog = os.path.basename(sys.argv[0])

        if result != None:
            try:
                return result.format(formatter=cls.out_formatters[clp.format])
            except KeyError, kerr:
                raise SystemExit('Cannot found a formatter for a %s' % clp.format)
