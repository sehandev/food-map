# -*- coding: utf-8 -*-

import re
import time
from twkorean import TwitterKoreanProcessor

processor = TwitterKoreanProcessor(normalization=False, stemming=False)
hangul = re.compile("[^ ㄱ-ㅣ가-힣]+")

result_file = open("../datas/josa_custom.txt", 'w')

def kakao_log_to_josa(kakao_file):

    with open(kakao_file, 'r') as file:
        lines = file.read().split('\n')

    josas = []

    for line in lines:
        # example : [KoreanToken(text='준비된', pos='Verb', unknown=False), ... ]
        tokens = processor.tokenize(line)

        for token in tokens:
            if token[1] == "Josa":
                josas.append(token[0])

    josas = list(set(josas))
    josas.sort(key=len)
    for josa in josas:
        result_file.write(josa + '\n')

if __name__ == "__main__":
    result = kakao_log_to_josa("../datas/kakao_processed_only_log.txt")
