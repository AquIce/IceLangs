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
        self.rules = {}
        self.languages = {}
        self.file_exceptions = []

    def get_all_files(self, act_dir:str=os.getcwd()) -> list:
        all_files = []
        self.list_files(act_dir, all_files)
        return all_files
        
    def list_files(self, dir_to_search_in:str, file_list:list) -> None:
        try:
            os.chdir(dir_to_search_in)
            for i in os.listdir(dir_to_search_in):
                if os.path.isdir(i):
                    self.list_files(i, file_list)
                elif os.path.isfile(i):
                    file_list.append(os.path.abspath(i))
                else:
                    raise NonHandledFileException
        except:
            pass

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

    def get_language_iteration(self, file_to_lang:list, i:str):
        for j in self.rules.keys():
            if i.split('.')[-1] == j.split('.')[-1]:
                file_to_lang[i] = self.rules[j]
                return
            else:
                file_to_lang[i] = 'Unknown'

    def get_language(self, file_to_check:list) -> dict:
        file_to_lang = {}
        for i in file_to_check:
            self.get_language_iteration(file_to_lang, i)
        return file_to_lang
        
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

    def calculate_percentage(self, dct:dict) -> dict:
        percentages = {}
        tot = self.char_sum(dct)
        for i in dct.keys():
            percentages[i] = dct[i] / tot * 100
        return percentages
        
    def print_percentages(self):
        for i in self.calculate_percentage(self.languages).keys():
            temp = self.calculate_percentage(self.languages)[i]
            if temp != 0:
                print(f'{i} : {temp:.2f}%')

    def run(self):
        self.load_rules('rules.txt')
        self.get_langs_chars(self.get_language(self.get_all_files()))
        self.print_percentages()