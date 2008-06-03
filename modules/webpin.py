class ScoutModule(object):

    name = "webpin"
    desc = "Search in the packages using the webpin webservice."

    @classmethod
    def main(cls):
        print "searching for term '%s'" % (sys.argv[1])

