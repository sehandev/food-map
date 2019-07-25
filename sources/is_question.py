from twkorean import TwitterKoreanProcessor
processor = TwitterKoreanProcessor()

from sources import manage_file

keyword_file = "./datas/question_keywords.txt"
keyword_dict = manage_file.read_txt_as_dict(keyword_file)
keyword_list = keyword_dict.keys()

def combine_tag(word):
    if word.count('!') + word.count('?') > 0:
        return '?'
    return word

def get_tokens(line):
    tokens = processor.tokenize_to_strings(line)

    for i in range(len(tokens)):
        text[i] = combine_tag(text[i])

    return tokens

def grade(line):
    score = 0
    tokens = get_tokens(line)
    for token in tokens:
        if token in keyword_list:
            score += keyword_dict[token]
    return score


