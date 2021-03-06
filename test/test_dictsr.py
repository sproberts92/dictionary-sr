import unittest
import os.path
import sqlite3

from dictsr import dbcore

class FunctionEnumTestCase(unittest.TestCase):
    def testEnumVaues(self):
        self.assertEqual(dbcore.Function.Noun.value, 1)
        self.assertEqual(dbcore.Function.Verb.value, 2)
        self.assertEqual(dbcore.Function.Adjective.value, 3)
        self.assertEqual(dbcore.Function.Adverb.value, 4)

class WordTestCase(unittest.TestCase):

    def setUp(self):
        self.test_word = dbcore.Word("Word", [("Fn1", "Def1"), ("Fn2", "Def2")])

    def tearDown(self):
        del self.test_word

    def test_init(self):
        self.assertEqual(self.test_word.word, "Word")
        self.assertEqual(self.test_word.definitions, [("Fn1", "Def1"), ("Fn2", "Def2")])

    def test_no_list_definitions(self):
        with self.assertRaises(TypeError):
            type_test = dbcore.Word("Word", "Function", "Def1")

    def test_add_definition(self):
        self.test_word.add_definition(('Fn3', 'Def3'))
        self.assertEqual(self.test_word.definitions, [("Fn1", "Def1"), ("Fn2", "Def2"), ('Fn3', 'Def3')])

def setUpDb(self, db):
    self.path = "test/databases/test.db"
    self.dirname = os.path.dirname(self.path)
    self.test_db = db(self.path)

def tearDownDb(self):
    self.test_db.conn.close()
    del self.test_db
    if os.path.exists(self.path):
        os.remove(self.path)
    if os.path.exists(self.dirname):
        os.rmdir(self.dirname)

class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        setUpDb(self, dbcore.Database)

    def tearDown(self):
        tearDownDb(self)

    def test_dir_init(self):
        self.assertTrue(os.path.isfile(self.path))

    def test_argument_types(self):
        with self.assertRaisesRegex(TypeError, "db_path must be a string"):
            database = dbcore.Database(1)

    def test_connection_type(self):
        self.assertIs(type(self.test_db.conn), sqlite3.Connection)

    def test_cursor_type(self):
        self.assertIs(type(self.test_db.c), sqlite3.Cursor)

class DictionarySetUpTestCase(unittest.TestCase):

    def setUp(self):
        setUpDb(self, dbcore.Dictionary)

    def tearDown(self):
        tearDownDb(self)

    def test_dir_init(self):
        self.assertTrue(os.path.isfile(self.path))

    def test_argument_types(self):
        with self.assertRaisesRegex(TypeError, "db_path must be a string"):
            test_dict = dbcore.Dictionary(1)

    def test_connection_type(self):
        self.assertIs(type(self.test_db.conn), sqlite3.Connection)

    def test_cursor_type(self):
        self.assertIs(type(self.test_db.c), sqlite3.Cursor)

    def test_table_creation(self):
        compare = [('table', 'dictionary', 'dictionary', 2)]

        self.test_db.c.execute('''
            SELECT type, name, tbl_name, rootpage
            FROM sqlite_master
        ''')

        self.assertEqual(self.test_db.c.fetchall(), compare)

    def test_create_when_table_already_exists(self):
        test_db = dbcore.Dictionary(self.path)

def setUpWord(self, word):
    self.test_word = dbcore.Word(word, [("Fn1", "Def1"), ("Fn2", "Def2")])

class DictionaryAddWordTestCase(unittest.TestCase):

    def setUp(self):
        setUpDb(self, dbcore.Dictionary)
        setUpWord(self, "Word")

    def tearDown(self):
        tearDownDb(self)

    def test_as_SQL_tuples(self):
        result = self.test_db.as_SQL_tuples(self.test_word)
        self.assertEqual(result, [("Word", "Fn1", "Def1"),("Word", "Fn2", "Def2")])

    def test_add_word(self):
        self.test_db.add_word(self.test_word)

        self.test_db.c.execute('''
            SELECT *
            FROM dictionary
        ''')

        self.assertEqual(
            self.test_db.c.fetchall(),
            self.test_db.as_SQL_tuples(self.test_word)
        )

    def test_uniqueness_of_entries(self):
        self.test_db.add_word(self.test_word)
        self.test_db.add_word(self.test_word)

        self.test_db.c.execute('''
            SELECT *
            FROM dictionary
        ''')

        self.assertEqual(
            self.test_db.c.fetchall(),
            self.test_db.as_SQL_tuples(self.test_word)
        )

class DictionaryGetWordTestCase(unittest.TestCase):
    def setUp(self):
        setUpDb(self, dbcore.Dictionary)
        setUpWord(self, "Word1")
        self.test_db.add_word(self.test_word)
        setUpWord(self, "Word2")
        self.test_db.add_word(self.test_word)

    def tearDown(self):
        tearDownDb(self)

    def test_get_word_from_db(self):
        extracted_words = self.test_db.get_word_list()

        self.assertEqual(set(extracted_words), set(['Word1', 'Word2']))

    def test_get_entry(self):
        entry = self.test_db.get_entry("Word2")

        self.assertEqual(entry.word, self.test_word.word)
        self.assertEqual(set(entry.definitions), set(self.test_word.definitions))

class DictionaryDeleteWordTestCase(unittest.TestCase):
    def setUp(self):
        setUpDb(self, dbcore.Dictionary)
        setUpWord(self, "Word1")
        self.test_db.add_word(self.test_word)
        setUpWord(self, "Word2")
        self.test_db.add_word(self.test_word)

    def tearDown(self):
        tearDownDb(self)

    def test_get_word_from_db(self):
        self.test_db.delete_entry(self.test_word.word)

        extracted_words = self.test_db.get_word_list()

        self.assertEqual(set(extracted_words), set(['Word1']))

    def test_get_entry(self):
        entry = self.test_db.get_entry("Word2")

        self.assertEqual(entry.word, self.test_word.word)
        self.assertEqual(set(entry.definitions), set(self.test_word.definitions))

if __name__ == '__main__':
    unittest.main()
