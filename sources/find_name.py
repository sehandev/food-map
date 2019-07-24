# -*- coding: utf-8 -*-

import re
import time
from twkorean import TwitterKoreanProcessor
from sources import manage_file

processor = TwitterKoreanProcessor(normalization=False, stemming=False)
hangul = re.compile("[^ 0-9가-힣]+")

josa_file = "/home/sehan/git/food-map/datas/josa_list.txt"
josa_list = manage_file.read_file_as_list(josa_file)

def kakao_log_to_nouns(sentence):

    names = set()  # 찾은 이름을 저장할 set
    line = hangul.sub(" ", sentence)

    # 1단계 : 띄어쓰기 기준
    words = line.split()
    for word in words:
        tmp = hangul.sub(" ", word).split()
        for word in tmp:
            names.add(word)

    # 2단계 : 명사 기준
    # example : [KoreanToken(text='준비된', pos='Verb', unknown=False), ... ]
    tokens = processor.tokenize(line)

    for token in tokens:
        if token[1] == "Noun":
            names.add(token[0])

    # 3단계 : 조사 기준
    for word in words:
        tokens = processor.tokenize(word)

        tmp = ""
        for token in tokens:
            if token[1] != "Josa":
                tmp += token[0]

        if tmp != "":
            names.add(tmp)

        # 제작된 조사 목록 기준
        for josa in josa_list:
            if word[-len(josa):] == josa:
                names.add(word)

    return list(names)


if __name__ == "__main__":

    names = kakao_log_to_nouns("백화양곱창도 좋아요!")
    print(names)
