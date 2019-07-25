from twkorean import TwitterKoreanProcessor
processor = TwitterKoreanProcessor()

from sources import manage_file

import re
hangul = re.compile("[^ !?가-힣]+")

keyword_file = "./datas/question_keywords.txt"
keyword_dict = manage_file.read_txt_as_dict(keyword_file)
keyword_list = keyword_dict.keys()

def combine_tag(word):
    if word.count('!') + word.count('?') > 0:
    # if word.count('?') > 0:
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
    tokens = get_tokens(line)
    
    if not '?' in tokens:
        score = -1
    else:
        for token in tokens:
            if token in keyword_list:
                score += float(keyword_dict[token])
                count += 1
                
        if count >= 1:
            score /= len(tokens)
            score = round(score, 2)
        else:
            score = 0
            
    return score


