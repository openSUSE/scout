# Copyright (c) 2008 Pavol Rusnak. Michal Vyskocil
# see __init__.py for license details

import gettext

import scout

_ = gettext.gettext


class ScoutModule(scout.SimpleScoutModule):

    name = 'autoconf'
    desc = _('Search for autoconf macros inside the m4 files.')
    sql = 'SELECT package, m4, macro FROM macros ' \
        'LEFT JOIN m4s ON macros.id_m4=m4s.id_m4 ' \
        'LEFT JOIN packages ON m4s.id_pkg=packages.id_pkg ' \
        'WHERE macro LIKE ?'
    sqli = 'SELECT package, m4, macro FROM macros ' \
        'LEFT JOIN m4s ON macros.id_m4=m4s.id_m4 ' \
        'LEFT JOIN packages ON m4s.id_pkg=packages.id_pkg ' \
        'WHERE package LIKE ?'
    scout.null_lang.install()
    result_list = [_('repo'), _('pkg'), _('m4'), _('macro')]
    result_list2 = [_('repository'), _('package'), _('m4 file'), _('macro')]
    scout.default_lang.install()
