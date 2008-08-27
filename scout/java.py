# Copyright (c) 2008 Pavol Rusnak, Michal Vyskocil
# see __init__.py for license details

import scout

class ScoutModule(scout.BasicScoutModule):

    name = "java"
    desc = _("Search for java classes inside the JAR files.")
    sql = 'SELECT package, jar, class FROM classes LEFT JOIN jars ON classes.id_jar=jars.id_jar LEFT JOIN packages ON jars.id_pkg=packages.id_pkg WHERE class LIKE ?'
    result_list = ['repo', 'pkg', 'jar', 'class']
    result_list2= ['repository', 'package', 'jar', 'class']
