#!/usr/bin/python

import os
import sys
import sqlite3

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
        print("")
        print("Usage: %s <module> <search_term> [module-options]" % (cls.prog))
        print("       - or -")
        print("       %s help <module> for module help" % (cls.prog))
        print("")
        print("available modules:")
        for module in cls.modules.values():
            print("\t%s\t%s" % (module.ScoutModule.name, module.ScoutModule.desc))
        print("")
        sys.exit(1)

    @classmethod
    def module_not_found(cls, name):
        print "Module '%s' not found" % (name)
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
        sys.path.append(dir)
        for file in os.listdir(dir):
            module_name, ext = os.path.splitext(file)
            if ext == '.py':
                module = __import__(module_name)
                cls.modules.append(module)

class Database(object):

    db = "db.sqlite"

    def __init__(self):
        if not os.path.exists(self.__class__.db):
            self.init()

        self.conn = sqlite3.connect(self.__class__.db)

    def init(self):
        self.conn = sqlite3.connect(self.__class__.db)
        self.conn.execute("""
CREATE TABLE distro (
    id          INT AUTO_INCREMENT,
    name        VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);
        """)
        self.conn.execute("""
CREATE TABLE rpm (
    id          INT AUTO_INCREMENT,
    name        VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY(id)
);        
        """)
        # FIXME: an imports
        self.conn.execute("""insert into distro VALUES(0, 'openSUSE:10.3')""")
        self.conn.execute("""insert into distro VALUES(1, 'Java:jpackage-1.7')""")
        self.conn.commit()
        self.conn.close()

    def __del__(self):
        self.conn.close()

    def _clever_query_result(self, c):
        ret = list()
        for row in c:
            if len(row) == 1:           #(2)
                ret.append(row[0])
            else:                       #(3)
                ret.append(row)
        if len(ret) == 1:                #(1)
            return ret[0]
        return ret

    def execute(self, query, *args, **kwargs):
        """
        an abstract database query - but more clever

        query - a query to proceed

        there're two kinds of placeholders (like as original DB/API execute, but in more Pythonic way)
        - question marks (qmark style):
          execute("SELECT ham, spam FORM foo WHERE bar=? and baz=?", bar, baz)
        - named placeholders (named style)
          execute("SELECT ham, spam FORM foo WHERE bar=:bar and baz=:baz", bar='42', baz='42')

        Note: its not possible to combine this two types of placeholders in one call!

        return
        (1) if the length of result is one, return one value
        (2) if the collumn in result is only one, return a list of values
        (3) else returns a list of tuples
        
        """

        # ther's not possible to use both a args and a keyword args
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

    def distros(self):
        """ return a list of distributions available in a database """
        return self.execute(""" SELECT name from distro;""")
    
    def has_distro(self, name):
        """ returns if the database contains specific distribution """
        return name in self.distros()

    def get_distro_id(self, name):
        """ return an ID of distribution """
        ret = -1
        ret = self.execute("""SELECT id from distro WHERE name=? """, name)
#        c = self.conn.cursor()
        # fixme - a filtering !!!
#        c.execute("""SELECT id from distro WHERE name='%s' """ % (name))
#        for row in c:
#            ret = row[0]
#        c.close()
        return ret

class ScoutCore(object):

    @classmethod
    def run(cls):

        ml = ModuleLoader
        ml.import_from(sys.path[0] + "/modules")

        clp = CommandLineParser(ml.modules)
        module = clp.parse()
        module.ScoutModule.main()

if __name__ == "__main__":
    ScoutCore.run()
