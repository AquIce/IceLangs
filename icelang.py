'''
 > Code by Icy
 > IceLangs Project
 > GitHub : 
'''

import os

rules = {}
languages = {}

class NonHandledFileException(Exception):
    def __init__(self, message='Try to open a non-handled file'):
        super().__init__(message)

def get_all_files(act_dir:str=os.getcwd()) -> list:
    all_files = []
    list_files(act_dir, all_files)
    return all_files
    
def list_files(dir_to_search_in:str, file_list:list) -> None:
    os.chdir(dir_to_search_in)
    for i in os.listdir(dir_to_search_in):
        if os.path.isdir(i):
            list_files(i)
        elif os.path.isfile(i):
            file_list.append(os.path.abspath(i))
        else:
            raise NonHandledFileException

def load_rules(rule_filename:str) -> None:
    with open(rule_filename, 'r') as f:
        content = f.readlines();
    for i in content:
        sep = i.split('->')
        lang = sep[1].replace('\n', '')
        rules[sep[0]] = lang
        languages[lang] = 0

def get_language_iteration(file_to_lang:list, i:str):
    for j in rules.keys():
        if i.split('.')[-1] == j.split('.')[-1]:
            file_to_lang[i] = rules[j]
            return
        else:
            file_to_lang[i] = 'Unknown'

def get_language(file_to_check:list) -> None:
    file_to_lang = {}
    for i in file_to_check:
        get_language_iteration(file_to_lang, i)
    return file_to_lang
    
def get_file_length():
    ...

def get_file_lang(file:str):
    ...

def get_all_files_length(files:list):
    for i in files:
        ...

def calculate_percentage():
    ...
    
def print_percentages():
    ...
    
if __name__ == '__main__':
    load_rules('a.txt')
    print(rules)
    dict = get_language(get_all_files())
    for i in dict.keys():
        print(i, 'is', dict[i])
