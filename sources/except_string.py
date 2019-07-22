except_file = "./datas/except_list.txt"
josa_file = "./datas/josa_list.txt"

with open(except_file, 'r') as file:
    except_list = file.read().split('\n')

with open(except_file, 'r') as file:
    except_list = file.read().split('\n')

def except_string(query):
    if len(query) > 2:
        if not query in except_list:

            return True
    return False