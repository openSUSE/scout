# The scout project
# Copyright (c) 2008 Pavol Rusnak, Michal Vyskocil
# This file is distributed under the terms of the MIT License
# see the comment at the end of this file

import fnmatch
import os
import sys
import sqlite3
from optparse import OptionParser, Option, OptionGroup, IndentedHelpFormatter, OptionValueError
from ConfigParser import SafeConfigParser

class Config(object):
    data_path = '/usr/share/scout'
    data_suffix = '.db'
    config_file = 'repos.conf'
    module_path = os.path.dirname(__file__)

# the auxiliary classes, which extend the optparse classes to be usefull for scout command line parsing
class HelpOptionFound(Exception):
    pass

class ExceptionHelpOption(Option):

    ACTIONS = Option.ACTIONS + ("help2", )

    def take_action(self, action, dest, opt, value, values, parser):
        if action == "help2":
            raise HelpOptionFound()
        else:
            Option.take_action(action, dest, opt, value, values, parser)

class ModuleListFormatter(IndentedHelpFormatter):
    """ Same as IndentedHelpFormatter, but the epilog is not a string, but the reference to a function"""

    def format_epilog(self, epilog):
        if epilog:
            return "\n" + epilog() + "\n"
        else:
            return ""


class CoreOptionParser(object):
    """
    This is a command-line parser for core. Just prints help for available
    modules and should return one a name of one of them.
    
    This is an accestor of older CommandLineParser with better design - usage
    of the optparse module, instead of the own parsing - and better support for
    unittesting.

    Instance (read-only) attributes:
        - prog:         a program name
        - module:       a name of selected module
        - module_args:  an arguments for modules
        - format:       an global option - output format
        - help:         a formatted help string

    Example:
        parser = CoreOptionParser(list_of_available_formats, list_of_available_modules)
        try:
            parser.parse_args()
        except HelpOptionFound help:
            parser.print_help()

        print "Selected module: %s" % (parser.module)
        print "Arguments for module: %s" % (parser.module_args)
    """

    def __init__(self, formats, modules=None):
        
        self._prog = os.path.basename(sys.argv[0])

        self._modules = list()
        self.add_module(modules)

        #defaults
        self._format = formats[0]

        #parser
        self._parser = OptionParser(
                prog = self._prog,
                usage = "usage: %prog [global_opts] module [local_opts] query",
                add_help_option = False,
                epilog = self._help_modules,
                formatter = ModuleListFormatter()
                )

        group = OptionGroup(self._parser, 'Global options')
        group.add_option(
                "-f", "--format",
                help="select the output format (default %s)" % (self._format),
                default=self._format,
                type="choice",
                choices=formats
                )
        group.add_option(
                ExceptionHelpOption(
                    "-h", "--help",
                    action="help2",
                    help="show this help message and exit"
                ))
        self._parser.add_option_group(group)

    def add_module(self, modules):
        if modules != None:
            if not hasattr(modules, "__iter__"):
                modules = (modules, )
            for m in modules:
                self._modules.append(m)
            self._modules.sort()
        return self
    
    def _help_modules(self):
        ret = "Available modules:\n"
        maxlen = len(max((m[0] for m in self._modules), key=len))
        for m in self._modules:
            ret += "    %s : %s\n" % (m[0].ljust(maxlen), m[1])
        return ret

    def _split_argument_line(self, args):
        # Splits the argument line to the tupe - (core_args, module_args)
        # ['scout',  '-f',  'xml',  'python',  'optparse'] -> (['scout'], ['-f'], ['xml']), (['python'], ['optparse'])
        # if none of the module name is defined, the module_args was empty
        module_i = -1
        for i, arg in enumerate(args):
            if arg in self._modules:
                module_i = i
                break
        if module_i == -1:
            return (args, [])
        return (args[:module_i], args[module_i:])

    def parse_args(self, args=None):
        """
        parse the arguments from sys.argv, or user defined ones!

        return - (args, values) as a standard OptionParser.parse_args method
        but it may raise:
            - HelpOptionFound: when the help string was found
            - OptionValueError: when the name of module was not found in command line
        for bad format argument it still use an optparse's sys.exit() method
        """
        # this line is necessary, the args=sys.argv[1:] in function definition seems doesn't works
        if not args:    args = sys.argv[1:]

        if len(args) == 0:      raise HelpOptionFound() # if none of the argument was defined, show help

        core_args, self._module_args = self._split_argument_line(args)
        
        # try to load the module name
        if len(self._module_args) != 0:
            self._module = self._module_args[0]

        ret = self._parser.parse_args(core_args)

        # no HelpOptionFound raised, the module name is mandatory
        if len(self._module_args) == 0:
            msg = 'The name of module is mandatory. Use %s --help' % (self._prog)
            raise OptionValueError(msg)

        # global options
        self._format = ret[0].format
        return ret

    def print_help(self, file=None):
        self._parser.print_help(file)
        return self

    # ------------------------------ read-only properties ------------------------------
    def __get_prog(self):
        return self._parser.prog
    prog = property(__get_prog)

    def __get_module(self):
        return self._module
    module = property(__get_module)

    def __get_module_args(self):
        return self._module_args[1:]
    module_args = property(__get_module_args)

    def __get_format(self):
        return self._format
    format = property(__get_format)

    def __get_help(self):
        return self._parser.format_help()
    help = property(__get_help)

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

    def get_usage(self):
        ret = """
Usage: %s [global_options] <module> <search_term> [module_options]

Global options:
\t-f FORMAT, --format=FORMAT    select the output format (default table)
\t-h, --help                    print help
\t-v, --version                 print version

available modules:
""" % (self.prog, )
        maxlen = len(max(self.modules.keys(), key=len))
        for k in sorted(self.modules.keys()):
            module = self.modules[k]
            ret += "    %s : %s\n" % (module.ScoutModule.name.ljust(maxlen), module.ScoutModule.desc)
        return ret

    def print_usage(self):
        print self.get_usage()
        sys.exit(1)

    def parse_option(self, short_opt, long_opt, default = None):
        opt = default
        if short_opt in sys.argv or long_opt in sys.argv:
            if long_opt in sys.argv:
                opt_index = sys.argv.index(long_opt)
            else:
                opt_index = sys.argv.index(short_opt)

            opt = sys.argv[opt_index]
            if opt[:2] == '--' and '=' in opt:
                _opt = s.split('=')[1]
                sys.argv.remove(opt)
                opt = _opt
            else:
                if len(sys.argv) == opt_index +1:
                    self.parse_error("You must specify a format. See scout --help")
                _opt = None
                _opt = sys.argv[opt_index + 1]
                sys.argv.remove(_opt)
                sys.argv.remove(opt)
                opt = _opt
        return opt

    def parse(self):

        if len(sys.argv) == 1 or (len(sys.argv) == 2 and self._is_help(sys.argv[1])):
            self.print_usage()

        self.__format = self.parse_option('-f', '--format', 'table')

        if len(sys.argv) <= 1:
            self.parse_error("You must specify a module name. See scout --help")
        mname = sys.argv[1]
        if not mname in self.modules:
            self.parse_error("Module '%s' was not found" % mname)
        del sys.argv[1]
        return self.modules[mname]

    def parse_error(self, msg, err_code=1):
        print msg
        sys.exit(err_code)

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
            if ext == '.py' and not (module_name == '__init__' or module_name == 'foo'):
                module = __import__(module_name)
                if not hasattr(module, 'ScoutModule'):
                    del module
                else:
                    cls.modules.append(module)

class Database(object):

    cursor = None

    def __init__(self, dbname):
        if dbname == ':memory:':
            dbfile = dbname
        else:
            if dbname.startswith('/'):
                # absolute path
                dbfile = dbname
            else:
                # only db name
                dbfile = Config.data_path + '/' + dbname + Config.data_suffix

        try:
            self.conn = sqlite3.connect(dbfile)
        except:
            print "Could not open database file '%s'" % dbfile
            self.conn = None

    def __del__(self):
        self.end()
        if self.conn != None:
            self.conn.close()

    def begin(self):
        if self.conn == None:
            return False
        self.cursor = self.conn.cursor()
        return True

    def execute(self, query, *args, **kwargs):
        # it is not possible to use both a args and a keyword args
        # self.cursor should also not be None at this point
        assert(len(args) == 0 or len(kwargs) == 0 or self.cursor == None)

        if len(args) == 0 and len(kwargs) == 0:
            self.cursor.execute(query)
        elif len(args) != 0:
            self.cursor.execute(query, args)
        else:
            self.cursor.execute(query, kwargs)

    def end(self):
       if self.cursor != None:
           self.cursor.close()
           self.cursor = None

    def query(self, query, *args, **kwargs):
        """
        an abstract database query - but more clever

        query - a query to proceed

        there're two kinds of placeholders (like as original DB/API execute, but in more Pythonic way)
        - question marks (qmark style):
          query("SELECT ham, spam FROM foo WHERE bar=? and baz=?", bar, baz)
        - named placeholders (named style)
          query("SELECT ham, spam FROM foo WHERE bar=:bar and baz=:baz", bar='42', baz='42')

        Note: its not possible to combine this two types of placeholders in one call!

        return
        (1) if the length of the result is one, returns one value
        (2) if the column in the result is the only one, returns a list of values
        (3) else returns a list of tuples
        """
        # TODO: do not return an sqlite3 Errors

        if not self.begin():
            return None

        self.execute(query, *args, **kwargs)

        # create clever result
        ret = list()
        for row in self.cursor:
            if len(row) == 1:           #(2)
                ret.append(row[0])
            else:                       #(3)
                ret.append(row)
        if len(ret) == 1:               #(1)
            ret = ret[0]

        self.end()

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
        if result.is_empty() : return ret
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
        if result.is_empty() : return ret
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

        ret = '<?xml version="1.0" encoding="UTF-8"?>\n'
        ret += '<%s>' % result_tag + '\n'
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
        ret.extend(self.rows)
        return ret

    def get_rows(self):
        return self.rows

    def is_empty(self):
        return len(self.rows) == 0

    def format(self, formatter=TableFormatter, **kwargs):
        return formatter.format(self, **kwargs)

class RepoConfigReader(object):
    """Class to read of an configuration of the repositories. This class
    internally uses SafeConfigParser for ConfigParser, but doesn't provide the
    same API"""

    def __init__(self):
        self.parser = SafeConfigParser()

    def read(self, file_name=None):
        """Read the config files and parse them. The files is loaded from
        directory ${Config.data_path}.  This should be suppressed by file_names
        argument.

        - file_name: is optional argument with a file name. The main purpose is
          for debugging.  """
        if file_name != None:
            self.parser.read([file_name, ])
        else:
            self.parser.read([os.path.join(Config.data_path, Config.config_file), ])
        return self

    def repos(self):
        return self.parser.sections()

    def has_repo(self, repo):
        return repo in self.parser.sections()

    def name(self, repo):
        return self.parser.get(repo, 'name')

    def baseurl(self, repo):
        return self.parser.get(repo, 'baseurl')

class Parser(object):

    def __init__(self, modulename):
        self.modulename = modulename
        self.parser = OptionParser(usage="Usage: %prog " + modulename + " [options] <search_term>")
        self.parser.add_option('-l', '--listrepos', action="store_true", help="list available repositories", dest="listrepo")
        self.parser.add_option('-r', '--repo', type='choice', help='select repository to search', default=None, choices=self.get_available_repos())

        self.repos_conf = RepoConfigReader().read()

    def add_repo(self, repo):
        opt = self.parser.get_option('-r')
        opt.choices.append(repo)

    def add_repos(self, repos):
        opt = self.parser.get_option('-r')
        for repo in repos:
            opt.choices.append(repo)

    # set repositories according to data files /usr/share/scout/<modulename>-*.db
    def get_available_repos(self):
        ret = list()
        for file in os.listdir(Config.data_path):
            if fnmatch.fnmatch(file, self.modulename + '-*' + Config.data_suffix):
                ret.append(file[len(self.modulename)+1:-len(Config.data_suffix)])
        return ret

    def format_available_repos(self):
        ret = "Available repositories:\n"
        if len(self.parser.get_option('-r').choices) == 0:
            ret += '- none -\n'
            return ret
        maxlen = len(max(self.parser.get_option('-r').choices, key=lambda x: x!=None and len(x) or 0))
        for opt in self.parser.get_option('-r').choices:
            if opt == None:
                continue
            if self.repos_conf.has_repo(opt):
                ret += opt.ljust(maxlen) + ' - ' + self.repos_conf.name(opt) + '\n'
                if self.repos_conf.baseurl(opt) != '':
                    ret += ' '*maxlen + '   * ' + self.repos_conf.baseurl(opt) + '\n'
            else:
                ret += opt + '\n'
        return ret

    def parse(self):
        (self.options, self.args) = self.parser.parse_args()
        if self.do_list():
            print self.format_available_repos()
            return False
        if len(self.args) == 0:
            self.parser.print_help()
            return False
        return True

    def get_repos(self):
        if self.options.repo:
            repos = [self.options.repo]
        elif self.parser.get_option('-r'):
            repos = [x for x in self.parser.get_option('-r').choices if x != None]
        else:
            repos = []
        if len(repos) == 0:
            print 'No repositories found ...'
            return None
        return repos

    def do_list(self):
        return self.options.listrepo

class BasicScoutModule(object):

    name = "name"
    desc = "desc"
    sql = "SQL"
    result_list = ['repo', 'pkg', 'module']
    result_list2= ['repository', 'package', 'module']

    @classmethod
    def query(cls, repo, term):
        db = Database(cls.name + '-' + repo)
        r = db.query(cls.sql, '%%%s%%' % term)
        if isinstance(r, list):
            return map( lambda x: [repo] + list(x), r)
        else:
            return [ [repo] + list(r) ]
        return r

    @classmethod
    def main(cls):
        p = Parser(cls.name)
        if not p.parse():
            return None
        term = p.args[0]

        result = Result( cls.result_list, cls.result_list2)

        repos = p.get_repos()
        if repos == None:
            return None
        for repo in repos:
            result.add_rows( cls.query(repo, term) )

        return result


class ScoutCore(object):

    out_formatters = {
            'csv' :     CSVFormatter,
            'xml' :     XMLFormatter,
            'table' :   TableFormatter,
            }

    @classmethod
    def run(cls):

        ml = ModuleLoader
        ml.import_from(Config.module_path)

        modules = ((m.ScoutModule.name, m.ScoutModule.desc) for m in ml.modules)
        clp = CoreOptionParser(cls.out_formatters.keys(), modules)
        try:
            args, values = clp.parse_args()
        except HelpOptionFound:
            clp.print_help()
            sys.exit(1)

        module_name = clp.module
        result = module.ScoutModule.main()

        prog = os.path.basename(sys.argv[0])

        if result != None:
            try:
                return result.format(formatter=cls.out_formatters[clp.format])
            except KeyError, kerr:
                raise SystemExit('Cannot find a formatter for a %s' % clp.format)


# Copyright (c) 2008 Pavol Rusnak, Michal Vyskocil
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
