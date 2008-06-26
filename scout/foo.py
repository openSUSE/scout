import scout

class ScoutModule(object):

    name = "foo"
    desc = "- template module -"

    @classmethod
    def main(cls):

        p = scout.Parser(cls.name)
        p.add_repos_from_datadir()
        if not p.parse():
            return None

        print p.get_repos()
        print p.args
        return None
