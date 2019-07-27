from twkorean import TwitterKoreanProcessor
import manage_file
import check_word
import compare_two_of_text
import except_list_of_place
import re
hangul = re.compile("[^ !?가-힣]+")
processor = TwitterKoreanProcessor()

first_file = "../datas/samples/kakao_questions.txt"
second_file = "../datas/kakao_log_left.txt"
# second_file = "../datas/unit_list.txt"
result_file1 = "../datas/compare_result.txt"
result_file2 = "../datas/only_question_result.txt"
rastaurant_file = "../datas/result.json"
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


def save_compare_result(compare_list, only_question_list):
    with open(result_file1, 'w') as file:
        for name, percent in compare_list:
            percent = round(percent, 2)
            file.write(name + " " + str(percent) + '\n')
        
    with open(result_file2, 'w') as file:
        for name, percent in only_question_list:
            percent = round(percent, 2)
            file.write(name + " " + str(percent) + '\n')        
    


def find_keywords():
    tokens = get_tokens(first_list)
    first_percent = check_word.count_words(tokens)
    tokens = get_tokens(second_list)
    second_percent = check_word.count_words(tokens)
    compare_list, only_question_list = compare_two_of_text.text_compare(first_percent, second_percent)
    save_compare_result(compare_list, only_question_list)

if __name__ == "__main__":
    find_keywords()
