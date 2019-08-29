import re
import time
from sources import datas

hangul = re.compile("[^ 0-9가-힣]+")


def kakao_log_to_nouns(sentence):

    nouns = list()  # 찾은 이름을 저장할 list
    line = hangul.sub(" ", sentence)

    # 1단계 : 띄어쓰기 기준
    words = line.split()
    nouns.extend(words)

    # 2단계 : 조사 기준
    for word in words:
        # 제작된 조사 목록 기준
        for josa in datas.josa_list:
            tmp_noun = word[-len(josa):]
            if tmp_noun == josa:
                nouns.append(tmp_noun)

    return list(set(nouns))


if __name__ == "__main__":
    nouns = kakao_log_to_nouns("백화양곱창도 좋아요!")
    print(nouns)
