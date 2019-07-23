import pathlib


def read_file(file_name):
    if pathlib.Path(file_name).exists():
        with open(file_name, 'r') as file:
            lines = file.read().split('\n')
        return lines
    else:
        print("There is no " + file_name.split('/')[-1])
        print("Return empty list")
        return []


def save_list_as_file(file_name, list):
    with open(file_name, 'w') as file:
        for element in list:
            file.write(element + '\n')
