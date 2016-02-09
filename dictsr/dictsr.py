import sqlite3 as sql
import os.path
from enum import Enum

class Function(Enum):
    Noun = 1
    Verb = 2
    Adjective = 3
    Adverb = 4

class Database:
    def __init__(self, db_path):
        if type(db_path) is str:
            dirname = os.path.dirname(db_path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            self.conn = sql.connect(db_path)
            self.c = self.conn.cursor()
        else:
            raise TypeError("db_path must be a string")

class Dictionary(Database):
    pass
    def __init__(self, database):
      super(Dictionary, self).__init__(database)

      self.c.execute('''
                      CREATE TABLE IF NOT EXISTS dictionary
                        (
                           word        TEXT,
                           function    TEXT,
                           definitions TEXT
                        )
                      ''')

class Word:
    def __init__(self, word, function, definitions):
        self.word = word
        self.function = function

        if type(definitions) is list:
            self.definitions = definitions
        else:
            raise TypeError("definitions must be a list of strings")
