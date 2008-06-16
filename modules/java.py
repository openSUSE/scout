import scout

class ScoutModule(object):

    name = "java"
    desc = "Search for the java classes inside the packaged JAR files."

    @classmethod
    def query(cls, repo, term):
        db = scout.Database(cls.name + '-' + repo)
        r = db.execute('SELECT package, jar, class FROM classes LEFT JOIN jars ON classes.id_jar=jars.id_jar LEFT JOIN packages ON jars.id_pkg=packages.id_pkg WHERE class LIKE ?', '%%%s%%' % term)
        result = scout.Result( ['pkg', 'jar', 'class'], ['package', 'jar', 'class']);

        if isinstance(r, list):
            for rr in r:
                result.addrow(rr)
        else:
           result.addrow(r)
        return result

    @classmethod
    def main(cls):

        p = scout.Parser(cls.name)
        p.add_repos_from_datadir()
        if not p.parse():
            return None
        repo = p.options.repo

        term = p.args[0]

        return cls.query(repo, term)
