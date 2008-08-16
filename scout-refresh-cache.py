#!/usr/bin/python

import sys
import scout
sys.path.append(scout.Config.module_path)
import bin

# refresh zypp satsolver repositories
if bin.satsolver != None:
    sp = bin.SolvParser()
    sp.refresh_cache()

