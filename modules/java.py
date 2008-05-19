from optparse import OptionParser
import re

class DBItem(object):

    def __init__(self, distro, rpm, jar, class_name):
        self.distro     = distro
        self.rpm        = rpm
        self.jar        = jar
        self.class_name = class_name

    def __getattr__(self, name):
        return self.__dict__[name]

class QueryOptions(object):

    def __init__(self, options, args):

        self.distro = options.distro
        self.terms = args

    def __getattr__(self, name):
        return self.__dict__[name]

    def __str__(self):

        return "{%s, %s}" % (self.distro, self.terms)


class PlainDatabaseModel(object):

    TYPEMAP  = {
            'distro' : 0,
            'rpm'    : 1,
            'jar'    : 2,
            'class'  : 3,
            }

    def __init__(self):

        self.db = [
                ("openSUSE:10.3", "ant-1.6.5-4jpp.noarch.rpm", "ant-1.6.5.jar", "org.apache.tools.zip.ZipShort"),
                ("Java:jpackage-1.7", "ant-1.7.0-30.noarch.rpm", "ant-1.7.0.jar", "org.apache.tools.zip.ZipShort"),
                ("openSUSE:10.3", "ant-1.6.5-4jpp.noarch.rpm", "ant-1.6.5.jar", "org.apache.tools.zip.ZipFile"),
                ("Java:jpackage-1.7", "ant-1.7.0-30.noarch.rpm", "ant-1.7.0.jar", "org.apache.tools.zip.ZipFile"),
                ("Java:jpackage-1.7", "ant-1.7.0-30.noarch.rpm", "ant-1.7.0.jar", "org.apache.tools.zip.ZipEntry")
                ]

    def _filter_row(self, row, filters):

        if "all" in filters:
            return row

        indexes = list()
        for f in filters:
            indexes.append(self.__class__.TYPEMAP[f])

        indexes.sort()

        ret = list()
        for i in indexes:
            ret.append(row[i])

        return ret


    def query(self, query):

        ret = list()

        for term in query.terms:

            pattern = re.compile(".*" + term + ".*")

            for row in (row for row in self.db if row[0] == query.distro):
                # FIXME: add an custom search option?
                #for item in self._filter_row(row, query.search):
                for item in row:
                    if pattern.match(item):
                        ret.append(row)


        return ret

    def get_distros(self):

        ret = set()

        for row in self.db:
            ret.add(row[0])

        return ret

class ClassParser(object):

    def __init__(self):

        self.parser = OptionParser(usage="Usage: %prog " + ScoutModule.name + " [options] class_name")
        # FIXME! this is an default Option for all parsers (some subtyping, or something else)
        self.parser.add_option("-d", "--distro", type="choice", help="information only from this distribution.", default="openSUSE:10.3", choices=["openSUSE:10.3", "Java:jpackage-1.7"])

    def parse_args(self):

        (options, args) = self.parser.parse_args()

        if len(args) == 0:
            self.parser.error("You must type a search term")

        return QueryOptions(options, args)

class ScoutModule(object):

    name = "java"
    desc = "Search for the java classes inside the packaged JAR files."

    model = PlainDatabaseModel

    @classmethod
    def main(cls, argv):
        """ a main method """

        p = ClassParser()
        query_opts = p.parse_args()

        m = cls.model()
        print m.query(query_opts)
