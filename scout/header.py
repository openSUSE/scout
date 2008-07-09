# Copyright (c) 2008 Michal Vyskocil
# see __init__.py for license details

import scout

class ScoutModule(scout.BasicScoutModule):

    name = "header"
    desc = "Search for the C/C++/Obj-C/Obj-C++ headers"
    sql = 'SELECT package, header FROM headers LEFT JOIN packages ON headers.id_pkg=packages.id_pkg WHERE header LIKE ?'