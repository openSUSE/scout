import scout


class ScoutModule(object):

    name = "java"
    desc = "Search for the java classes inside the packaged JAR files."

    @classmethod
    def main(cls):
        """ a main method """

        p = scout.Parser(cls.name)
        if not p.parse():
            return None

        print p.options
        print p.args
