from twkorean import TwitterKoreanProcessor
import manage_file
import check_word
import compare_two_of_text
import except_list_of_place
import re
hangul = re.compile("[^ !?가-힣]+")
processor = TwitterKoreanProcessor()

first_file = "/home/sehan/git/food-map/datas/samples/kakao_questions_2.txt"
# second_file = "/home/sehan/git/food-map/datas/kakao_log.txt"
second_file = "/home/sehan/git/food-map/datas/unit_list.txt"
result_file = "/home/sehan/git/food-map/datas/compare_result.txt"
rastaurant_file = "/home/sehan/git/food-map/datas/result.json"
first_list = manage_file.read_file_as_list(first_file)
second_list = manage_file.read_file_as_list(second_file)
subway_list = except_list_of_place.except_place()
rastuarant_list = manage_file.read_json_as_dict(rastaurant_file).keys()


def get_tokens(lines):
    result_list = []
    for line in lines:
        line = hangul.sub(" ", line)
        for subway in subway_list:
            line = line.replace(subway, "지역")
        for rastuarant in rastuarant_list:
            line = line.replace(rastuarant, "이름")
        tokens = processor.tokenize_to_strings(line)
        for token in tokens:
            result_list.append(token)

    return result_list


def save_compare_result(compare_list):
    with open(result_file, 'w') as file:
        for name, percent in compare_list:
            percent = round(percent, 2)
            file.write(name + " " + str(percent) + '\n')


def find_keywords():
    tokens = get_tokens(first_list)
    first_percent = check_word.count_words(tokens)
    tokens = get_tokens(second_list)
    second_percent = check_word.count_words(tokens)
    compare_list = compare_two_of_text.text_compare(first_percent, second_percent)
    save_compare_result(compare_list)


if __name__ == "__main__":
    find_keywords()
