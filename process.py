#!/usr/bin/python

import os

file = '/usr/share/java/libgcj-4.3.jar'

jarlist = os.popen('fastjar tf %s' % (file))
for line in jarlist:
    if not line.endswith('.class\n') or line.find('$') >= 0:
        continue
    print line[:-7].replace('/','.')
jarlist.close()
