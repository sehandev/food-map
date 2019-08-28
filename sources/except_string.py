from sources import datas

def except_string(query):
    # 3글자 미만, 숫자, 숫자+단위, 블랙리스트, 검색기록 있음 -> 제외
    if len(query) > 2:  # 길이 3 이상
        if not query.isdigit():  # 숫자만 있지 않으면
            # if 숫자 + 단위
            for unit in datas.unit_list:  # 각 단위에 대해서
                if query[:-len(unit)].isdigit():  # (숫자 +)
                    if query[-len(unit):] == unit:  # (+ 단위)
                        return True  # 제외

            if not query in datas.except_list:  # 블랙리스트에 없으면
                if not query in datas.already_list:  # 이미 검색한 기록이 없으면
                    datas.already_list.append(query)  # 검색한 기록이 없으므로 추가
                    return False  # 추가

    # 길이 3 미만 or 숫자
    return True  # 제외
