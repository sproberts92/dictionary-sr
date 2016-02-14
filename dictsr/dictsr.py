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

class Word:
    def __init__(self, word, definitions):
        self.word = word

        if type(definitions) is list:
            self.definitions = definitions
        else:
            raise TypeError('definitions must be a list of strings')

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
        self.view.insert_into_text_area('Select a definition from the list or add a new one.')

    def populate_word_list(self):
        self.view.set_word_list(self.model.get_word_list())

    def list_item_selected(self, not_needed):
        selection = self.view.get_list_selection();
        word = self.model.get_word(selection)
        self.view.insert_word_into_text_area(word)

class View(tk.Frame):    
    def __init__(self, vc):
        self.vc = vc
        self.root = tk.Tk()

        self.loadView()
    
    def loadView(self):
        self.menubar = tk.Menu(self.root)
        self.menubar.add_command(label='File')
        self.root.config(menu=self.menubar)

        self.word_list = tk.Listbox(self.root)
        self.word_list.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.word_list.bind('<Double-Button-1>', self.vc.list_item_selected)

        self.text_area = tk.Text(self.root, state=tk.DISABLED)
        self.text_area.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

    def init_data(self):
        pass

    def get_list_selection(self):
        items = self.word_list.curselection()
        return self.word_list.get(items)

    def set_word_list(self, words):
        for w in words:
            self.word_list.insert(tk.END, w)

    def format_word_as_text(self, word):
        string = '{0}\n\n'.format(word.word)
        for defn in word.definitions:
            string += '{0}\n'.format(defn[0])
            string += '{0}\n\n'.format(defn[1])
        return string

    def insert_into_text_area(self, text):
        self.text_area.configure(state=tk.NORMAL)
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, text)
        self.text_area.configure(state=tk.DISABLED)

    def insert_word_into_text_area(self, word):
        string = self.format_word_as_text(word)
        self.insert_into_text_area(string)

class Model:
    def __init__(self, vc):
        self.dict = Dictionary('databases/financialance.db')
        word = Word('Security', [('Noun', 'A tradeable financial asset, such as a share of stock'), ('Noun', 'Proof of ownership of stocks, bonds or other investment instruments.')])
        self.dict.add_word(word)
        word = Word('Stock', [('Noun', 'The capital raised by a company through the issue of shares. The total of shares held by an individual shareholder. ')])
        self.dict.add_word(word)

    def get_word_list(self):
        return self.dict.get_word_list()

    def get_word(self, name):
        return self.dict.get_entry(name)

def main():
    app = Controller()
    app.view.root.mainloop()

if __name__ == '__main__':
    main()
