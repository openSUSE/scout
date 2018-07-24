#!/usr/bin/env python3

# A tests for scout
#

from copy import copy
from optparse import OptionValueError
import sys
import unittest
sys.path.insert(0, '../scout/')
import scout

if not hasattr(scout, 'ScoutCore'):
    raise ImportError('No main scout module found')


class CoreOptionParserTestCase(unittest.TestCase):

    def setUp(self):
        self.argv_bak = copy(sys.argv)
        sys.argv = ['scout']

        self.modules = (('python', 'Search for python modules'),
                        ('java', 'Search for java classes'))
        self.formats = ('table', 'xml', 'csv')
        self.parser = scout.CoreOptionParser(self.formats, self.modules)

    def tearDown(self):
        sys.argv = copy(self.argv_bak)

    def testInit(self):
        self.assertEqual(self.parser.prog, 'scout')
        self.assertEqual(self.parser._format, 'table')

    def testNoArgs(self):
        try:
            self.parser.parse_args()
        except scout.HelpOptionFound:
            pass
        else:
            self.fail('The HelpOptionFound have to be raised '
                      'for no defined argument')

    def testHelp(self):
        sys.argv.append('--help')
        try:
            self.parser.parse_args()
        except scout.HelpOptionFound:
            pass
        else:
            self.fail('The HelpOptionFound have to be raised')

        # just try to get a help, it's not necessary to test the
        # excplicit content of the help string test of snippet would
        # be enough
        help = self.parser.help
        self.assertTrue(len(help) != 0)
        self.assertTrue(help.find('Usage') == 0)
        self.assertTrue(help.find('python') > 1)

    def testModule(self):
        for m in [m[0] for m in self.modules]:
            sys.argv = ['scout', m, 'foo']

            self.parser.parse_args()

            self.assertEqual(self.parser._format, 'table')
            self.assertEqual(self.parser.module, m)
            self.assertEqual(len(self.parser.module_args), 1)
            self.assertEqual(self.parser.module_args[0], 'foo')

    def testFormatOption(self):
        for format in self.formats:
            sys.argv = ['scout', '--format', format, 'python']

            self.parser.parse_args()
            self.assertEqual(self.parser._format, format)

# This test doesn't works, because OptionParser calls a sys.exit() and
# that's not catchable thing in Python :-(
# FIXME: a redefine of the parse_args method in OptionParser subclass
#        but this is not really interesting for normal use, only for
#        testing
#    def testUnknownFormatOption(self):
#        sys.argv = ['scout', '--format', '__unknown_format__', 'python']
#
#        try:
#            self.parser.parse_args()
#        except SystemExit:
#            pass

    def testNonExistingModule(self):
        # TODO
        sys.argv = ['scout', 'non-existing']
        try:
            self.parser.parse_args()
        except OptionValueError:
            pass
        else:
            self.fail('The command line parsing have to fails '
                      'on the non-existinig module.')


suite = unittest.makeSuite(CoreOptionParserTestCase, 'test')

runner = unittest.TextTestRunner()
runner.run(suite)
