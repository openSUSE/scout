# Copyright (c) 2008 Pavol Rusnak
# see __init__.py for license details

import scout

class ScoutModule(scout.BasicScoutModule):

    name = "library"
    desc = "Search for C/C++/Obj-C/Obj-C++ libraries"
    sql = 'SELECT package, library FROM libraries LEFT JOIN packages ON libraries.id_pkg=packages.id_pkg WHERE library LIKE ?'
