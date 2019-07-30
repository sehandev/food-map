import pathlib
import json


def read_file_as_list(file_name):
    if pathlib.Path(file_name).exists():
        with open(file_name, 'r', encoding='utf-8-sig') as file:
            lines = file.read().split('\n')
        return lines
    else:
        print("There is no [ " + file_name.split('/')[-1] + " ]")
        print("Return empty list")
        return []


def save_list_as_file(file_name, list):
    with open(file_name, 'w') as file:
        for element in list:
            file.write(str(element) + '\n')


def read_json_as_dict(file_name):
    if pathlib.Path(file_name).exists():
        with open(file_name, encoding='utf-8-sig') as file:
            dict = json.load(file)
        return dict
    else:
        print("There is no [ " + file_name.split('/')[-1] + " ]")
        print("Return empty dict")
        return {}


def save_dict_as_json(file_name, dict):
    with open(file_name, 'w', encoding='utf-8-sig') as file:
        json.dump(dict, file, ensure_ascii=False, indent=2)


def read_txt_as_dict(file_name):
    if pathlib.Path(file_name).exists():
        with open(file_name, encoding='utf-8-sig') as file:
            tmp_dict = {}
            lines = file.read().split('\n')
            for line in lines:
                # line example : name 1.23
                tmp_list = line.split()
                tmp_dict[tmp_list[0]] = tmp_list[1]
            return tmp_dict
    else:
        print("There is no [ " + file_name.split('/')[-1] + " ]")
        print("Return empty dict")
        return {}
