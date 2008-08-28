# Copyright (c) 2008 Pavol Rusnak, Michal Vyskocil
# see __init__.py for license details

import scout

class ScoutModule(scout.BasicScoutModule):

    name = "java"
    desc = _("Search for java classes inside the JAR files.")
    sql = 'SELECT package, jar, class FROM classes LEFT JOIN jars ON classes.id_jar=jars.id_jar LEFT JOIN packages ON jars.id_pkg=packages.id_pkg WHERE class LIKE ?'
    scout.NullLang.install()
    result_list = [_("repo"), _("pkg"), _("jar"), _("class")]
    scout.DefaultLang.install()
    result_list2= [_("repository"), _("package"), _("jar"), _("class")]
