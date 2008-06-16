import scout

class ScoutModule(object):

    name = "java"
    desc = "Search for the java classes inside the packaged JAR files."

    @classmethod
    def query(cls, repo, term):
        db = scout.Database(cls.name + '-' + repo)
        r = db.execute('SELECT package, jar, class FROM classes LEFT JOIN jars ON classes.id_jar=jars.id_jar LEFT JOIN packages ON jars.id_pkg=packages.id_pkg WHERE class LIKE ?', '%%%s%%' % term)
        if isinstance(r, list):
            return map( lambda x: [repo] + list(x), r)
        else:
            return [ [repo] + list(r) ]
        return r

    @classmethod
    def main(cls):

        p = scout.Parser(cls.name)
        p.add_repos_from_datadir()
        if not p.parse():
            return None
        term = p.args[0]

        result = scout.Result( ['repo', 'pkg', 'jar', 'class'], ['repository', 'package', 'jar', 'class']);

        for repo in p.get_repos():
            result.add_rows( cls.query(repo, term) )

        return result
