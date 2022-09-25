'''
 > Code by Icy
 > IceLangs Project
 > GitHub : https://github.com/LilTim0/IceLangs
'''

import os

class NonHandledFileException(Exception):
    def __init__(self, message='Try to open a non-handled file'):
        super().__init__(message)

class IceLang:
    def __init__(self, rulefile:str) -> None:
        self.rulefile = rulefile
        self.all_files = []
        self.rules = {}
        self.languages = {}
        self.file_to_lang = {}
        self.file_exceptions = []
          
    # Lists the files
    def list_files(self, dir_to_search_in:str=os.getcwd()) -> None:
        os.chdir(os.path.abspath(dir_to_search_in))
        dir_list = []
        for i in os.listdir(os.getcwd()):
            try:
                if os.path.isdir(i):
                    dir_list.append(i)
                elif os.path.isfile(i):
                    self.all_files.append(os.path.abspath(i))
                else:
                    raise NonHandledFileException
            except: ...
        for j in dir_list:
            try:
                self.list_files(os.path.abspath(j))
            except: ...

    # Loads the rules
    def load_rules(self, rule_filename:str) -> None:
        self.file_exceptions.append(os.path.abspath(rule_filename))
        with open(rule_filename, 'r') as f:
            content = f.readlines()
        for i in content:
            if not i.startswith('#'):
                sep = i.split('->')
                lang = sep[1].replace('\n', '')
                self.rules[sep[0]] = lang
                self.languages[lang] = 0
        self.languages['Unknown'] = 0

    # Adds language to self.file_lang
    def get_language_iteration(self, i:str):
        for j in self.rules.keys():
            if i.split('.')[-1] == j.split('.')[-1]:
                self.file_to_lang[i] = self.rules[j]
                return
            else:
                self.file_to_lang[i] = 'Unknown'

    # Apply self.get_language_iteration to each file
    def get_language(self) -> None:
        for i in self.all_files:
            self.get_language_iteration(i)
        
    def get_file_length(self, filename:str) -> int:
        with open(filename, 'r') as f:
            return len(f.read())

    def get_file_lang(self, file:str, dct:dict) -> dict:
        for i in dct.keys():
            if i == file:
                return dct[i]

    def get_langs_chars(self, dct:dict) -> None:
        for i in dct.keys():
            if not i in self.file_exceptions:
                self.languages[self.get_file_lang(i, dct)] += self.get_file_length(i)

    def char_sum(self, dct:dict) -> int:
        total = 0
        for i in dct.keys():
            total += dct[i]
        return total

    def get_file_by_lang(self):
        for i in self.file_to_lang.keys():
            for j in self.rules.keys():
                ...

    def calculate_percentage(self) -> dict:
        percentages = {}
        tot = self.char_sum(self.languages)
        for i in self.languages.keys():
            percentages[i] = self.languages[i] / tot * 100
        return percentages
        
    def print_percentages(self) -> None:
        for i in self.calculate_percentage().keys():
            temp = self.calculate_percentage()[i]
            if temp != 0:
                print(f'{i} : {temp:.2f}%')

    def run(self):
        self.load_rules('rules.txt')
        self.list_files()
        self.get_language()
        self.get_langs_chars(self.file_to_lang)
        self.print_percentages()
