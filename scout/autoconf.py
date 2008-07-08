# Copyright (c) 2008 Pavol Rusnak
# see __init__.py for license details

import scout

class ScoutModule(object):

    name = "autoconf"
    desc = "Search for autoconf macros inside the m4 files."

    @classmethod
    def query(cls, repo, term):
        db = scout.Database(cls.name + '-' + repo)
        r = db.execute('SELECT package, m4, macro FROM macros LEFT JOIN m4s ON macros.id_m4=m4s.id_m4 LEFT JOIN packages ON m4s.id_pkg=packages.id_pkg WHERE macro LIKE ?', '%%%s%%' % term)
        if r == None:
            return None
        if isinstance(r, list):
            return map( lambda x: [repo] + list(x), r)
        else:
            return [ [repo] + list(r) ]
        return r

    @classmethod
    def main(cls):

        p = scout.Parser(cls.name)
        if not p.parse():
            return None
        term = p.args[0]

        result = scout.Result( ['repo', 'pkg', 'm4', 'macro'], ['repository', 'package', 'm4 file', 'macro']);

        for repo in p.get_repos():
            result.add_rows( cls.query(repo, term) )

        return result
