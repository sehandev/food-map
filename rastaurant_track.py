import json
import pathlib
import signal

from sources import preprocessing, find_name, except_string, naver_local, manage_file

kakao_file = "/home/sehan/git/food-map/datas/kakao.txt"
already_file = "/home/sehan/git/food-map/datas/already_list.txt"


def tracking():
    processed_lines = preprocessing.preprocessing(kakao_file)  # [ [시간1, 이름1, 내용1], [시간2, 이름2, 내용2], ... ]

    count = 1
    for sentence in processed_lines:
        names = find_name.kakao_log_to_nouns(sentence[2])
        for name in names:
            if not except_string.except_string(name):
                results = naver_local.check_name(name)
                if results == -1:
                    print("네이버 지역 검색 API 할당량을 초과했습니다")
                    return
                elif results != []:
                    print("name : " + name)
                    print(*results, sep='\n')
                    print()
        count += 1
        if count % 50 == 0:
            manage_file.save_list_as_file(already_file, except_string.get_already_list())
            print("count : " + str(count))


    manage_file.save_list_as_file(already_file, except_string.get_already_list())
    print("검색 완료")


if __name__ == "__main__":
    tracking()
