# Copyright (c) 2008 Pavol Rusnak, Michal Vyskocil
# see __init__.py for license details

import scout

class ScoutModule(scout.SimpleScoutModule):

    name = "java"
    desc = _("Search for java classes inside the JAR files.")
    sql  = 'SELECT package, jar, class FROM classes LEFT JOIN jars ON classes.id_jar=jars.id_jar LEFT JOIN packages ON jars.id_pkg=packages.id_pkg WHERE class LIKE ?'
    sqli = 'SELECT package, jar, class FROM classes LEFT JOIN jars ON classes.id_jar=jars.id_jar LEFT JOIN packages ON jars.id_pkg=packages.id_pkg WHERE package LIKE ?'
    scout.null_lang.install()
    result_list  = [_("repo"), _("pkg"), _("jar"), _("class")]
    result_list2 = [_("repository"), _("package"), _("jar"), _("class")]
    scout.default_lang.install()

    # make scout java be usable with some/package/Class.class arguments
    def prepare_term(self, term):
        if term.find('/') == -1:
            return term

        if term[-6:] == '.class':
            term = term[:-6]

        return term.replace('/', '.')
