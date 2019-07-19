import json

import find_name
import preprocessing
import naver_local

kakao_file = "../datas/kakao.txt"

def tracking():
    processed_lines = preprocessing.preprocessing(kakao_file)  # [ [시간1, 이름1, 내용1], [시간2, 이름2, 내용2], ... ]
    for sentence in processed_lines:
        print(sentence)
        names = find_name.kakao_log_to_nouns(sentence)
        for name in names:
            if len(name) > 2:
                naver_local.check_name(name)

if __name__ == "__main__":
    tracking()
