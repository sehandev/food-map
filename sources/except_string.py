from sources import manage_file

except_file = "/home/sehan/git/food-map/datas/except_list_2.txt"
josa_file = "/home/sehan/git/food-map/datas/josa_list.txt"
already_file = "/home/sehan/git/food-map/datas/already_list.txt"
unit_file = "/home/sehan/git/food-map/datas/unit_list.txt"

except_list = manage_file.read_file_as_list(except_file)
josa_list = manage_file.read_file_as_list(josa_file)
already_list = manage_file.read_file_as_list(already_file)
unit_list = manage_file.read_file_as_list(unit_file)



def except_string(query):
    if len(query) < 3:  # 길이 3 미만
        if query.isdigit():  # 숫자만 있으면
            # 숫자 + 단위면
            for unit in unit_list:
                if query[-len(unit):] == unit:
                    if query[:-len(unit)].isdigit():
                        return True

    if query in already_list:  # 이미 검색한 기록이 있으면
        if query in except_list:  # 블랙리스트에 있으면
            return True

    already_list.append(query)  # 검색한 기록이 없으므로 추가
    return False


def get_already_list():
    return already_list
