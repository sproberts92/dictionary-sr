import unittest
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

if __name__ == '__main__':
    unittest.main()
