import unittest
import os.path
import time
import sqlite3

from dictsr import dictsr

class FunctionEnumTestCase(unittest.TestCase):
    def testEnumVaues(self):
        self.assertEqual(dictsr.Function.Noun.value, 1)
        self.assertEqual(dictsr.Function.Verb.value, 2)
        self.assertEqual(dictsr.Function.Adjective.value, 3)
        self.assertEqual(dictsr.Function.Adverb.value, 4)

class WordTestCase(unittest.TestCase):

    def setUp(self):
        self.test_word = dictsr.Word("Word", [("Fn1", "Def1"), ("Fn2", "Def2")])

    def tearDown(self):
        del self.test_word

    def test_init(self):
        self.assertEqual(self.test_word.word, "Word")
        self.assertEqual(self.test_word.definitions, [("Fn1", "Def1"), ("Fn2", "Def2")])

    def test_no_list_definitions(self):
        with self.assertRaises(TypeError):
            type_test = dictsr.Word("Word", "Function", "Def1")

class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.path = "test/databases/test_db"
        self.dirname = os.path.dirname(self.path)
        self.database = dictsr.Database(self.path)

    def tearDown(self):
        del self.database
        if os.path.exists(self.path):
            os.remove(self.path)
        if os.path.exists(self.dirname):
            os.rmdir(self.dirname)

    def test_dir_init(self):
        self.assertTrue(os.path.isfile(self.path))

    def test_argument_types(self):
        with self.assertRaisesRegex(TypeError, "db_path must be a string"):
            database = dictsr.Database(1)

    def test_connection_type(self):
        self.assertIs(type(self.database.conn), sqlite3.Connection)

    def test_cursor_type(self):
        self.assertIs(type(self.database.c), sqlite3.Cursor)

class DictionarySetUpTestCase(unittest.TestCase):

    def setUp(self):
        self.path = "test/databases/test_db"
        self.dirname = os.path.dirname(self.path)
        self.test_dict = dictsr.Dictionary(self.path)

    def tearDown(self):
        del self.test_dict
        if os.path.exists(self.path):
            os.remove(self.path)
        if os.path.exists(self.dirname):
            os.rmdir(self.dirname)

    def test_dir_init(self):
        self.assertTrue(os.path.isfile(self.path))

    def test_argument_types(self):
        with self.assertRaisesRegex(TypeError, "db_path must be a string"):
            test_dict = dictsr.Dictionary(1)

    def test_connection_type(self):
        self.assertIs(type(self.test_dict.conn), sqlite3.Connection)

    def test_cursor_type(self):
        self.assertIs(type(self.test_dict.c), sqlite3.Cursor)

    def test_table_creation(self):
        compare = [('table', 'dictionary', 'dictionary', 2)]

        self.test_dict.c.execute('''
            SELECT type, name, tbl_name, rootpage
            FROM sqlite_master
        ''')

        self.assertEqual(self.test_dict.c.fetchall(), compare)

    def test_create_when_table_already_exists(self):
        test_db = dictsr.Dictionary(self.path)

class DictionaryAddWordTestCase(unittest.TestCase):

    def setUp(self):
        self.path = "test/databases/test_db"
        self.dirname = os.path.dirname(self.path)
        self.test_dict = dictsr.Dictionary(self.path)
        self.test_word = dictsr.Word("Word", [("Fn1", "Def1"), ("Fn2", "Def2")])

    def tearDown(self):
        del self.test_dict
        if os.path.exists(self.path):
            os.remove(self.path)
        if os.path.exists(self.dirname):
            os.rmdir(self.dirname)

    def test_as_SQL_tuples(self):
        result = self.test_dict.as_SQL_tuples(self.test_word)
        self.assertEqual(result, [("Word", "Fn1", "Def1"),("Word", "Fn2", "Def2")])

    def test_add_word(self):
        self.test_dict.add_word(self.test_word)

        self.test_dict.c.execute('''
            SELECT *
            FROM dictionary
        ''')

        self.assertEqual(
            self.test_dict.c.fetchall(),
            self.test_dict.as_SQL_tuples(self.test_word)
        )

    def test_uniqueness_of_entries(self):
        self.test_dict.add_word(self.test_word)
        self.test_dict.add_word(self.test_word)

        self.test_dict.c.execute('''
            SELECT *
            FROM dictionary
        ''')

        self.assertEqual(
            self.test_dict.c.fetchall(),
            self.test_dict.as_SQL_tuples(self.test_word)
        )

if __name__ == '__main__':
    unittest.main()
