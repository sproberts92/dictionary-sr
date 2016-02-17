import tkinter as tk
import dbcore


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

    def add_word_callback(self):
        pass

    def add_defn_callback(self):
        pass

        # name = self.view.tl_word.entry.get()
        # word = Word(name, [])

        # self.model.add_word(word)
        # self.populate_word_list()


class View_pop_up(tk.Frame):
    def __init__(self, parent, vc, title):
        self.vc = vc
        self.tl = tk.Toplevel(parent)
        self.tl.title(title)
        self.load_view()

    def load_view(self):
        # Word name box
        self.tl.entry = tk.Entry(self.tl, width=35)
        self.tl.entry.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        
        # Select box for word type
        self.tl.var = tk.StringVar()
        self.tl.var.set('Select word type')
        
        self.tl.word_function = tk.OptionMenu(self.tl, self.tl.var, *[e.name for e in dbcore.Function])
        self.tl.word_function.config(width=15)
        self.tl.word_function.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

        # Definition entry
        self.tl.text_area = tk.Text(self.tl, width=35, font=("Helvetica",9))
        self.tl.text_area.grid(row=2, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

        # Add button
        self.tl.add_button = tk.Button(self.tl, text='Add', command=self.vc.add_word_callback)
        self.tl.add_button.grid(row=3, column=0, columnspan=2)

        # Grid config
        self.tl.columnconfigure(0, weight=1)
        self.tl.rowconfigure(2, weight=1)


class View_add_word(View_pop_up):
    def __init__(self, parent, vc):
        super(View_add_word, self).__init__(parent, vc, 'Add word')
        self.loadView()


class View_add_defn(View_pop_up):
    def __init__(self, parent, vc):
        super(View_add_defn, self).__init__(parent, vc, 'Add definition')


class View(tk.Frame):
    def __init__(self, vc):
        self.vc = vc
        self.root = tk.Tk()
        self.root.title('Dictionary')
        self.loadView()

    def loadView(self):
        self.menubar = tk.Menu(self.root)
        self.menubar.add_command(label='File')
        self.root.config(menu=self.menubar)

        self.word_list = tk.Listbox(self.root)
        self.word_list.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.word_list.bind('<Double-Button-1>', self.vc.list_item_selected)

        self.text_area = tk.Text(self.root, state=tk.DISABLED, font=("Helvetica",9))
        self.text_area.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

        self.button_add_word = tk.Button(self.root, text='Add word', command=self.create_view_add_word)
        self.button_add_word.grid(row=2, column=0)

        self.button_add_definition = tk.Button(self.root, text='Add definition', command=self.create_view_add_defn)
        self.button_add_definition.grid(row=2, column=1)

        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

    def create_view_add_word(self):
        self.view_add_word = View_add_word(self.root, self.vc)

    def create_view_add_defn(self):
        self.view_add_defn = View_add_defn(self.root, self.vc)

    def get_list_selection(self):
        items = self.word_list.curselection()
        return self.word_list.get(items)

    def set_word_list(self, words):
        self.word_list.delete(0, tk.END)
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
        self.dict = dbcore.Dictionary('databases/financialance.db')
        word = dbcore.Word('Security', [('Noun', 'A tradeable financial asset, such as a share of stock'), ('Noun', 'Proof of ownership of stocks, bonds or other investment instruments.')])
        self.dict.add_word(word)
        word = dbcore.Word('Stock', [('Noun', 'The capital raised by a company through the issue of shares. The total of shares held by an individual shareholder. ')])
        self.dict.add_word(word)

    def get_word_list(self):
        return self.dict.get_word_list()

    def get_word(self, name):
        return self.dict.get_entry(name)

    def add_word(self, word):
        print(word.word)
        # word.definitions=[('','')]
        self.dict.add_word(word)
