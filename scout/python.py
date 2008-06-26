import scout

class ScoutModule(object):

    name = "python"
    desc = "Search for the python modules."

    @classmethod
    def query(cls, repo, term):
        db = scout.Database(cls.name + '-' + repo)
        r = db.execute('SELECT package, module FROM modules LEFT JOIN packages ON modules.id_pkg=packages.id_pkg WHERE module LIKE ?', '%%%s%%' % term)
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

        result = scout.Result( ['repo', 'pkg', 'module'], ['repository', 'package', 'module']);

        for repo in p.get_repos():
            result.add_rows( cls.query(repo, term) )

        return result
