#!/usr/bin/env python3

# Copyright (c) 2008 Pavol Rusnak, Michal Vyskocil
# see __init__.py for license details

import scout
import hotshot
import hotshot.stats


def runscout():
    scout.ScoutCore.load_all_modules()

    ret = scout.ScoutCore.run()
    if ret is not None:
        print(ret, end=' ')


prof = hotshot.Profile('scout.prof')
prof.runcall(runscout)
prof.close()

stats = hotshot.stats.load('scout.prof')
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)
