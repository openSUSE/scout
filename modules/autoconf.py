import scout
import sys

class ScoutModule(object):

    name = "autoconf"
    desc = "Search for autoconf macros inside the m4 files."

    @classmethod
    def main(cls):
        print "searching for term '%s'" % (sys.argv[1])

