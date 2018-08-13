# Copyright (c) 2008 Michal Vyskocil
# see __init__.py for license details

import gettext

import scout

_ = gettext.gettext


class ScoutModule(scout.SimpleScoutModule):

    name = 'header'
    desc = _('Search for C/C++/Obj-C/Obj-C++ headers.')
    sql = 'SELECT package, header FROM headers ' \
        'LEFT JOIN packages ON headers.id_pkg=packages.id_pkg ' \
        'WHERE header LIKE ?'
    sqli = 'SELECT package, header FROM headers ' \
        'LEFT JOIN packages ON headers.id_pkg=packages.id_pkg ' \
        'WHERE package LIKE ?'
    scout.null_lang.install()
    result_list = [_('repo'), _('pkg'), _('header')]
    result_list2 = [_('repository'), _('package'), _('header')]
    scout.default_lang.install()
