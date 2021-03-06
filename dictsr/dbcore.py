import os.path
import sqlite3 as sql
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
            raise TypeError('db_path must be a string')

class Dictionary(Database):
    def __init__(self, database):
        super(Dictionary, self).__init__(database)

        self.c.execute('''
            CREATE TABLE IF NOT EXISTS dictionary
            (
                word        TEXT,
                function    TEXT,
                definition  TEXT
            )
        ''')

    def as_SQL_tuples(self, word):
        tuples = [(word.word, a, b) for a, b in word.definitions]
        return tuples

    def add_word(self, word):
        self.c.execute('''
            SELECT *
            FROM dictionary
            WHERE word = '{w}'
        '''.format(w=word.word))

        current_words = self.c.fetchall()
        to_insert = [w for w in self.as_SQL_tuples(word) 
                     if w not in current_words]

        self.c.executemany('INSERT INTO dictionary VALUES (?,?,?)', to_insert)

        self.conn.commit()

    def get_word_list(self):
        self.c.execute('''
            SELECT word
            FROM dictionary
        ''')

        extr_words = [x[0] for x in self.c.fetchall()]

        return list(set(extr_words))

    def get_entry(self, word_str):
        self.c.execute('''
            SELECT *
            FROM dictionary
            WHERE word = '{w}'
        '''.format(w=word_str))

        return Word.from_SQL_tuple(self.c.fetchall())

    def delete_entry(self, word_str):
        self.c.execute('''
            DELETE 
            FROM dictionary
            WHERE word = '{w}'
        '''.format(w=word_str))

class Word:
    def __init__(self, word, definitions):
        self.word = word

        if type(definitions) is list:
            self.definitions = definitions
        else:
            raise TypeError('definitions must be a list')

    @classmethod
    def from_SQL_tuple(cls, sql_tuple):
        
        name = sql_tuple[0][0]
        defs = [(x[1], x[2]) for x in sql_tuple]

        return cls(name, defs)

    def add_definition(self, definition):
        self.definitions.append(definition)