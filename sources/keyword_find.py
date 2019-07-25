import manage_file
import check_word
import compare_two_of_text
from twkorean import TwitterKoreanProcessor
processor = TwitterKoreanProcessor()

first_file = "../datas/kakao_questions.txt"
second_file = "../datas/kakao_log.txt"
result_file = "../datas/compare_result.txt"
first_list = manage_file.read_file_as_list(first_file)
second_list = manage_file.read_file_as_list(second_file)


def get_tokens(lines):
    result_list = []
    for line in lines:
        tokens = processor.tokenize_to_strings(line)
        for token in tokens:
            result_list.append(token)

    return result_list

def print_compare_result(compare_list):
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
    print_compare_result(compare_list)

if __name__ == "__main__":
    find_keywords()
