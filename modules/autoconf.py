import scout

class ScoutModule(object):

    name = "autoconf"
    desc = "Search for autoconf macros inside the m4 files."

    @classmethod
    def query(cls, repo, term):
        db = scout.Database(cls.name + '-' + repo)
        r = db.execute('SELECT package, m4, macro FROM macros LEFT JOIN m4s ON macros.id_m4=m4s.id_m4 LEFT JOIN packages ON m4s.id_pkg=packages.id_pkg WHERE macro LIKE ?', term)
        result = scout.Result( ['pkg', 'm4', 'macro'], ['package', 'm4 file', 'macro']);

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
