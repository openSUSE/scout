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

        self.prog = sys.argv[0]

    def add_module(self, module):
        self.modules[module.Info.name] = module

    def _is_help(self, arg):
        for help in ("help", "-h", "-help", "--help"):
            if arg == help:
                return True
        return False

    def print_usage(self):
        print("Usage: %s module searchTerm" % (self.prog))
        print("       %s help module or %s module help for help" % (self.prog, self.prog))
        print("")
        print("available modules:")
        for module in self.modules.values():
            print("\t%s\t%s" % (module.Info.name, module.Info.descr))

        sys.exit(1)


    def parse(self):

        if len(sys.argv) == 1 or (len(sys.argv) == 2 and self._is_help(sys.argv[0])):
            self.print_usage()

        mname = sys.argv[1]
        if not mname in self.modules:
            # fixme - and exception?
            self.print_module_error(mname)

        del sys.argv[1]         # delete a module name for argument list
        return self.modules[mname]


class ModuleLoader(object):
    """
    The basic module loader - it allows to load a module from specified directory(ies)
    """

    modules = list()

    @classmethod
    def import_modules(cls, dirs):
        ret = list()
        _dirs = dirs

        # make an non-iter item as iter
        if not hasattr(dirs, "__iter__"):
            _dirs = (dirs, )
            
        for dir in _dirs:
            ret.extend(cls._import(dir))
        
        return ret

    @classmethod
    def _import(cls, dir):

        adir = os.path.abspath(dir)

        if not os.path.isdir(adir):
            raise AttributeError("%s is not a directory" % dir)

        sys.path.append(adir)

        for file in os.listdir(adir):
            module_name, ext = os.path.splitext(file)
            if ext == '.py':
                #log.info('import %s' % module_name)
                module = __import__(module_name)
                cls.modules.append(module)

        return cls.modules

modules = ModuleLoader.import_modules("modules")
parser = CommandLineParser(modules)

module = parser.parse()

ret = module.Info.main(sys.argv)

print ret
