import re
from sources import datas

hangul = re.compile("[^ !?0-9가-힣]+")


def grade(line):
    score = 0
    count = 0

    line = hangul.sub(" ", line)  # 기호(!?), 한글, 숫자만 남기기
    for place in datas.place_list:
        line = line.replace(place, " 지역 ")
    for restaurant in datas.restaurant_list:
        line = line.replace(restaurant, " 이름 ")
    for food in datas.food_list:
        line = line.replace(food, " 음식 ")
    line = line.replace('!', ' ! ')
    line = line.replace('?', ' ? ')

    tokens = line.split()

    # 질문 키워드에 포함되면 check
    check_list = [0 for i in range(len(datas.keyword_list))]
    for token in tokens:
        for i in range(len(datas.keyword_list)):
            if token[0:len(datas.keyword_list[i])] == datas.keyword_list[i]:
                check_list[i] = float(datas.keyword_dict[datas.keyword_list[i]])

    # check 점수, 개수 확인
    for check in check_list:
        if check != 0:
            score += check
            count += 1

    # 점수 평균
    if count > 2:
        score /= len(tokens)
        score = round(score, 2)
    else:
        score = 0

    return score
