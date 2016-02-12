import sqlite3 as sql
import os.path
import tkinter as tk
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

class Word:
    def __init__(self, word, definitions):
        self.word = word

        if type(definitions) is list:
            self.definitions = definitions
        else:
            raise TypeError("definitions must be a list of strings")

    @classmethod
    def from_SQL_tuple(cls, sql_tuple):
        
        name = sql_tuple[0][0]
        defs = [(x[1], x[2]) for x in sql_tuple]

        return cls(name, defs)

class Controller:
    def __init__(self):
        self.model = Model(self)
        self.view  = View(self)

        self.populate_word_list()
        self.populate_definition()

    def populate_word_list(self):
        self.view.set_word_list(self.model.get_word_list())

    def populate_definition(self):
        self.view.insert_into_text_area("Three")

class View(tk.Frame):    
    def __init__(self, vc):
        self.vc = vc
        self.root = tk.Tk()

        self.loadView()
    
    def loadView(self):
        self.word_list = tk.Listbox(self.root)
        self.word_list.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        self.text_area = tk.Text(self.root, state=tk.DISABLED)
        self.text_area.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

    def init_data(self):
        pass

    def set_word_list(self, words):
        for w in words:
            self.word_list.insert(tk.END, w)

    def insert_into_text_area(self, text):
        self.text_area.configure(state=tk.NORMAL)
        self.text_area.insert(tk.END, text)
        self.text_area.configure(state=tk.DISABLED)

class Model:
    def __init__(self, vc):
        pass
        
    def get_word_list(self):
        return ['One', 'Two']

    def get_word(self):
        pass

def main():
    app = Controller()
    app.view.root.mainloop()

if __name__ == '__main__':
    main()
