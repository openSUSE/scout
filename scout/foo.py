# Copyright (c) 2008 Pavol Rusnak, Michal Vyskocil
# see __init__.py for license details

import scout

class ScoutModule(object.BasicScoutModule):

    name = "foo"
    desc = "- template module -"
    sql = 'SELECT package, @@FOO@@, @@BAR@@ FROM @@BAR@@s LEFT JOIN @@FOO@@s ON @@BAR@@s.id_@@FOO@@=@@FOO@@s.id_@@FOO@@ LEFT JOIN packages ON @@FOO@@s.id_pkg=packages.id_pkg WHERE @@BAR@@ LIKE ?', '%%%s%%'
    result_list = ['repo', 'pkg', '@@FOO@@', '@@BAR@@']
    result_list2= ['repository', 'package', '@@FOO@@ file', '@@BAR@@']

