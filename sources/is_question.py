import re
from sources import manage_file, except_list_of_place
from twkorean import TwitterKoreanProcessor

processor = TwitterKoreanProcessor()
hangul = re.compile("[^ !?가-힣]+")

keyword_file = "./datas/question_keywords.txt"
rastaurant_file = "./datas/result.json"
keyword_dict = manage_file.read_txt_as_dict(keyword_file)
keyword_list = keyword_dict.keys()
subway_list = except_list_of_place.except_place()
rastuarant_list = manage_file.read_json_as_dict(rastaurant_file).keys()


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
    tokens = get_tokens(line)

    if not '?' in tokens:
        score = -1
    else:
        for token in tokens:
            if token in keyword_list:
                score += float(keyword_dict[token])
                count += 1

        if count > 1:
            score /= len(tokens)
            score = round(score, 2)
        else:
            score = 0

    return score
