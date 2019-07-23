import pathlib
import json


def read_file_as_list(file_name):
    if pathlib.Path(file_name).exists():
        with open(file_name, 'r') as file:
            lines = file.read().split('\n')
        return lines
    else:
        print("There is no [ " + file_name.split('/')[-1] + " ]")
        print("Return empty list")
        return []


def save_list_as_file(file_name, list):
    with open(file_name, 'w') as file:
        for element in list:
            file.write(element + '\n')


def read_json_as_dict(file_name):
    if pathlib.Path(file_name).exists():
        with open(file_name) as file:
            dict = json.load(file)
        return dict
    else:
        print("There is no [ " + file_name.split('/')[-1] + " ]")
        print("Return empty dict")
        return {}


def save_dict_as_json(file_name, dict):
    with open(file_name, 'w', encoding='utf8') as file:
        json.dump(dict, file, ensure_ascii=False, indent=2)
