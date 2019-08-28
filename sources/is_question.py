import re
from sources import datas

hangul = re.compile("[^ !?0-9가-힣]+")


def combine_tag(word):
    if word.count('!') + word.count('?') > 0:
        return '?'
    return word


def grade(line):
    score = 0
    count = 0

    line = hangul.sub(" ", line)  # 기호(!?), 한글, 숫자만 남기기
    for place in datas.place_list:
        line = line.replace(place, "지역")
    for restaurant in datas.restaurant_list:
        line = line.replace(restaurant, "이름")
    for food in datas.food_list:
        line = line.replace(food, "음식")
    tokens = line.split()

    already_check = [0 for i in range(len(datas.keyword_list))]
    for token in tokens:
        for i in range(len(datas.keyword_list)):
            if token == datas.keyword_list[i]:
                already_check[i] = float(datas.keyword_dict[token])

    for check in already_check:
        if check > 0:
            score += check
            count += 1

    if count > 1:
        score /= len(tokens)
        score = round(score, 2)
    else:
        score = 0

    return score, tokens
