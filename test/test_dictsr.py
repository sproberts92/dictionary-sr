import unittest
import os.path
import time
import sqlite3

from dictsr import dictsr

class WordTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.test_word = dictsr.Word("Word", "Function", ["Def1", "Def2"])

    @classmethod
    def tearDownClass(self):
        del self.test_word

    def test_init(self):
        self.assertEqual(self.test_word.word, "Word")
        self.assertEqual(self.test_word.function, "Function")
        self.assertEqual(self.test_word.definitions, ["Def1", "Def2"])

    def test_no_list_definitions(self):
        with self.assertRaises(TypeError):
            type_test = dictsr.Word("Word", "Function", "Def1")

class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.path = "test/databases/test_db"
        self.dirname = os.path.dirname(self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)
        if os.path.exists(self.dirname):
            os.rmdir(self.dirname)

    def test_dir_init(self):
        database = dictsr.Database(self.path)
        self.assertTrue(os.path.isfile(self.path))

    def test_argument_types(self):
        with self.assertRaisesRegex(TypeError, "db_path must be a string"):
            database = dictsr.Database(1)

    def test_connection_type(self):
        database = dictsr.Database(self.path)
        self.assertIs(type(database.conn), sqlite3.Connection)

    def test_cursor_type(self):
        database = dictsr.Database(self.path)
        self.assertIs(type(database.c), sqlite3.Cursor)

if __name__ == '__main__':
    unittest.main()
