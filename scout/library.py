# Copyright (c) 2008 Pavol Rusnak
# see __init__.py for license details

import gettext

import scout

_ = gettext.gettext


class ScoutModule(scout.SimpleScoutModule):

    name = 'library'
    desc = _('Search for shared libraries.')
    sql = 'SELECT package, library FROM libraries ' \
        'LEFT JOIN packages ON libraries.id_pkg=packages.id_pkg ' \
        'WHERE library LIKE ?'
    sqli = 'SELECT package, library FROM libraries ' \
        'LEFT JOIN packages ON libraries.id_pkg=packages.id_pkg ' \
        'WHERE package LIKE ?'
    scout.null_lang.install()
    result_list = [_('repo'), _('pkg'), _('library')]
    result_list2 = [_('repository'), _('package'), _('library')]
    scout.default_lang.install()
