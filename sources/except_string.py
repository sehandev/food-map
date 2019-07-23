from sources import manage_file

except_file = "/home/sehan/git/food-map/datas/except_list.txt"
josa_file = "/home/sehan/git/food-map/datas/josa_list.txt"
already_file = "/home/sehan/git/food-map/datas/already_list.txt"

except_list = manage_file.read_file(except_file)
josa_list = manage_file.read_file(josa_file)
already_list = manage_file.read_file(already_file)


def except_string(query):
    if len(query) > 2:
        if not query.isdigit():
            if not query in already_list:
                already_list.append(query)
                if not query in except_list:
                    return True
    return False


def get_already_list():
    return already_list
