import json

from sources import find_name, preprocessing, naver_local, except_string

kakao_file = "./datas/kakao.txt"

def tracking():
    processed_lines = preprocessing.preprocessing(kakao_file)  # [ [시간1, 이름1, 내용1], [시간2, 이름2, 내용2], ... ]
    for sentence in processed_lines:
        names = find_name.kakao_log_to_nouns(sentence[2])
        for name in names:
            if not except_string(name):
                results = naver_local.check_name(name)
                if results == -1:
                    print("네이버 지역 검색 API 할당량을 초과했습니다")
                    return
                elif results != []:
                    print()
                    print(*results, sep='\n')

if __name__ == "__main__":
    tracking()
