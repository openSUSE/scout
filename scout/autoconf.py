# Copyright (c) 2008 Pavol Rusnak. Michal Vyskocil
# see __init__.py for license details

import scout

class ScoutModule(scout.BasicScoutModule):

    name = "autoconf"
    desc = _("Search for autoconf macros inside the m4 files.")
    sql = 'SELECT package, m4, macro FROM macros LEFT JOIN m4s ON macros.id_m4=m4s.id_m4 LEFT JOIN packages ON m4s.id_pkg=packages.id_pkg WHERE macro LIKE ?', '%%%s%%'
    scout.null_lang.install()
    result_list = [_("repo"), _("pkg"), _("m4"), _("macro")]
    result_list2= [_("repository"), _("package"), _("m4 file"), _("macro")]
    scout.default_lang.install()
