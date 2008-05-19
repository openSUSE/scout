#!/usr/bin/python

import os
import sys

# this is a comment

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
