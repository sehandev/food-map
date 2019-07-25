import manage_file
import check_word
import compare_two_of_text
from twkorean import TwitterKoreanProcessor
processor = TwitterKoreanProcessor()

first_file = "../datas/kakao_questions.txt"
second_file = "../datas/kakao_questions.txt"
first_list = manage_file.read_file_as_list(first_file)
second_list = manage_file.read_file_as_list(second_file)


def get_tokens(lines):
    result_list = []
    for line in lines:
        tokens = processor.tokenize_to_strings(line)
        for token in tokens:
            result_list.append(token)

    return result_list


def find_keywords():
    tokens = get_tokens(first_list)
    first_percent = check_word.count_word(tokens)
    tokens = get_tokens(second_list)
    second_percent = check_word.count_word(tokens)
    compare_two_of_text.compare_between(first_percent, second_percent)


if __name__ == "__main__":
    find_keywords()
