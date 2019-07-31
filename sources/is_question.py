import re
from sources import manage_file, except_list_of_place
from twkorean import TwitterKoreanProcessor

processor = TwitterKoreanProcessor()
hangul = re.compile("[^ !?0-9가-힣]+")

keyword_file = "./datas/question_keywords.txt"
restaurant_file = "./results/restaurant.json"
food_file = "./datas/food_list.txt"

keyword_dict = manage_file.read_txt_as_dict(keyword_file)
keyword_list = list(keyword_dict.keys())
subway_list = except_list_of_place.except_place()
rastuarant_list = manage_file.read_json_as_dict(restaurant_file).keys()
food_list = manage_file.read_file_as_list(food_file)


def combine_tag(word):
    if word.count('!') + word.count('?') > 0:
        return '?'
    return word


def get_tokens(line):
    tokens = processor.tokenize_to_strings(line)

    for i in range(len(tokens)):
        tokens[i] = combine_tag(tokens[i])

    return tokens


def grade(line):
    score = 0
    count = 0

    line = hangul.sub(" ", line)
    for subway in subway_list:
        line = line.replace(subway, "지역")
    for rastuarant in rastuarant_list:
        line = line.replace(rastuarant, "이름")
    for food in food_list:
        line = line.replace(food, "음식")
    tokens = get_tokens(line)

    # if not '?' in tokens:
    #     score = -1
    # else:
    already_check = [0 for i in range(len(keyword_list))]
    for token in tokens:
        for i in range(len(keyword_list)):
            if token == keyword_list[i]:
                already_check[i] = float(keyword_dict[token])

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
