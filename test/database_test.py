#!/usr/bin/python

# A tests for scout
#

import sqlite3
import sys
import unittest

sys.path.insert(0, '../scout/')
import scout
if not hasattr(scout, 'ScoutCore'):
    raise ImportError('No main scout module found')


class SimpleDatabaseTestCase(unittest.TestCase):

    def _check_simple_results_row(self, row):
        self.assertEqual(len(row), 2)
        self.assertEqual(type(row[0]), type(u''))
        self.assertEqual(type(row[1]), type(u''))
        self.assertEqual(row[0], row[1].split('-')[0])

    def setUp(self):
        self.database = scout.Database(':memory:')

        self.database.begin()
        c = self.database.cursor

        self.term = 'package3-module2'
        self.sql_begin = 'SELECT package, module ' \
            'FROM modules LEFT JOIN packages ON modules.id_pkg=packages.id_pkg'

        sql = """
CREATE TABLE modules (id_modules INT PRIMARY KEY NOT NULL, module VARCHAR(64) NOT NULL, id_pkg INT NOT NULL);
CREATE TABLE packages(id_pkg INT PRIMARY KEY NOT NULL, package VARCHAR(64) NOT NULL);
INSERT INTO packages(id_pkg, package) VALUES(1, 'package1');
INSERT INTO packages(id_pkg, package) VALUES(2, 'package2');
INSERT INTO packages(id_pkg, package) VALUES(3, 'package3');
INSERT INTO modules(id_modules, module, id_pkg) VALUES(1, 'package1-module1', 1);
INSERT INTO modules(id_modules, module, id_pkg) VALUES(2, 'package1-module2', 1);
INSERT INTO modules(id_modules, module, id_pkg) VALUES(3, 'package1-module3', 1);
INSERT INTO modules(id_modules, module, id_pkg) VALUES(4, 'package2-module1', 2);
INSERT INTO modules(id_modules, module, id_pkg) VALUES(5, 'package2-module2', 2);
INSERT INTO modules(id_modules, module, id_pkg) VALUES(6, 'package2-module3', 2);
INSERT INTO modules(id_modules, module, id_pkg) VALUES(7, 'package3-module1', 3);
INSERT INTO modules(id_modules, module, id_pkg) VALUES(8, 'package3-module2', 3);
INSERT INTO modules(id_modules, module, id_pkg) VALUES(9, 'package3-module3', 3);
CREATE INDEX modules_module_idx ON modules(module);
"""

        for cmd in sql.splitlines():
            c.execute(cmd)

    def tearDown(self):
        del self.database

    def testExecuteString(self):
        sql = self.sql_begin + " WHERE module LIKE '%%%s%%'" % self.term

        res = self.database.execute(sql)
        self._check_simple_results_row(res)

        self.assertEqual(self.term.split('-')[0], res[0])
        self.assertEqual(self.term, res[1])

    def testExecutePlaceholders1(self):
        sql = self.sql_begin + ' WHERE module LIKE ?'

        res = self.database.execute(sql, '%'+self.term+'%')
        self._check_simple_results_row(res)

        self.assertEqual(self.term.split('-')[0], res[0])
        self.assertEqual(self.term, res[1])

    def testExecutePlaceholders2(self):
        sql = self.sql_begin + ' WHERE module LIKE :module'

        res = self.database.execute(sql, module='%'+self.term+'%')
        self._check_simple_results_row(res)

        self.assertEqual(self.term.split('-')[0], res[0])
        self.assertEqual(self.term, res[1])

    def testCleverResults(self):
        # return of a [[, ], [, ], [, ]]
        sql = self.sql_begin

        res = self.database.execute(sql)

        self.assertEqual(type(res), type(list()))
        self.assertTrue(len(res) >= 0)
        self.assertTrue(type(res[0]), type(tuple()))
        self.assertEqual(len(res[0]), 2)
        for i in range(len(res)):
            self.assertEqual(type(res[i][0]), type(str()))
            self.assertEqual(type(res[i][1]), type(str()))

        sql = 'SELECT module FROM modules'

        res = self.database.execute(sql)

        self.assertEqual(type(res), type(list()))
        self.assertTrue(len(res) >= 0)
        for i in range(len(res)):
            self.assertEqual(type(res[i]), type(str()))

        sql = 'SELECT module FROM modules ' \
            "WHERE module='package1-module1'"

        res = self.database.execute(sql)
        self.assertEqual(type(res), type(str()))
        self.assertEqual(res, 'package1-module1')

    def testUsageOfBothPlaceholders(self):

        sql = self.sql_begin + ' WHERE module LIKE ? OR module LIKE :module'

        try:
            self.database.execute(sql, 'module', module='module')
        except AssertionError:
            pass
        else:
            msg = 'The execute module disallows usage of both placeholders!'
            self.fail(msg)

    def testIncorrectSQLCommand(self):
        sql = 'NOT_SQL_COMMAND'

        try:
            self.database.execute(sql)
        except sqlite3.OperationalError:
            pass
        else:
            self.fail('The %s is not an SQL command' % sql)

        sql = self.sql_begin + ' WHERE module LIKE ?'
        try:
            self.database.execute(sql, module='module1')
        except sqlite3.ProgrammingError:
            pass
        else:
            self.fail('The ? is not working with keyword args')

        sql = self.sql_begin + ' WHERE module LIKE :module'
        # FIXME!!! The sqlite3 doesn't return an error
        # try:
        #     self.database.execute(sql, 'module1')
        # except sqlite3.ProgrammingError:
        #     pass
        # else:
        #     self.fail('The ? is not working with keyword args')


suiteDatabase = unittest.makeSuite(SimpleDatabaseTestCase, 'test')

runner = unittest.TextTestRunner()
runner.run(suiteDatabase)
