# Copyright (c) 2008 Michal Vyskocil
# see __init__.py for license details

import scout

class ScoutModule(scout.BasicScoutModule):

    name = "python"
    desc = _("Search for python modules.")
    sql = 'SELECT package, module FROM modules LEFT JOIN packages ON modules.id_pkg=packages.id_pkg WHERE module LIKE ?'
