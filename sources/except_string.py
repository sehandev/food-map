from sources import manage_file

josa_file = "./datas/josa_list.txt"
already_file = "./datas/already_list.txt"
unit_file = "./datas/unit_list.txt"

josa_list = manage_file.read_file_as_list(josa_file)  # 조사
already_list = manage_file.read_file_as_list(already_file)  # 검색기록
unit_list = manage_file.read_file_as_list(unit_file)  # 단위

except_file = "./datas/except_list.txt"
food_file = "./datas/food_list.txt"
subway_file = "./datas/subway_station.txt"
place_file = "./datas/place_name.txt"

except_list = manage_file.read_file_as_list(except_file)  # 사용자 제작
subway_list = manage_file.read_file_as_list(subway_file)  # 지하철 역명
food_list = manage_file.read_file_as_list(food_file)  # 음식 이름
place_list = manage_file.read_file_as_list(place_file)  # 지역명

except_list.extend(subway_list)
except_list.extend(food_list)
except_list.extend(place_list)


def except_string(query):
    # 3글자 미만, 숫자, 숫자+단위, 블랙리스트, 검색기록 있음 -> 제외
    if len(query) > 2:  # 길이 3 이상
        if not query.isdigit():  # 숫자만 있지 않으면
            # if 숫자 + 단위
            for unit in unit_list:  # 각 단위에 대해서
                if query[:-len(unit)].isdigit():  # (숫자 +)
                    if query[-len(unit):] == unit:  # (+ 단위)
                        return True  # 제외

            if not query in except_list:  # 블랙리스트에 없으면
                if not query in already_list:  # 이미 검색한 기록이 없으면
                    already_list.append(query)  # 검색한 기록이 없으므로 추가
                    return False  # 추가

    # 길이 3 미만 or 숫자
    return True  # 제외


def get_already_list():
    return already_list
