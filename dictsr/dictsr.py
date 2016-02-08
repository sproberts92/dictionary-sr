class Word:
    def __init__(self, word, function, definitions):
        self.word = word
        self.function = function

        if type(definitions) is list:
            self.definitions = definitions
        else:
            raise TypeError("definitions must be a list of strings")
