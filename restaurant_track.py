from sources import preprocessing, find_name, except_string, naver_local, manage_file, is_question
import time
import signal
import pathlib
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--track", help="tracking restaurant name", action="store_true")
parser.add_argument("--grade", help="grading questions", action="store_true")
parser.add_argument("--match", help="find match of question and answer", action="store_true")
args = parser.parse_args()


# kakao_file = "./datas/kakao.txt"
kakao_file = "./datas/ADE_test_2.txt"
# kakao_file = "./datas/ADE_test_3.txt"
already_file = "./datas/already_list.txt"
track_result_file = "./results/restaurant.json"
grade_result_file = "./results/grade.txt"
match_result_file = "./results/match.txt"


def track_name():
    # kakao_file에서 식당명 찾기
    t_time = time.time()  # 시작 시간

    processed_lines = preprocessing.preprocessing(kakao_file)  # [ [시간1, 이름1, 내용1], [시간2, 이름2, 내용2], ... ]
    result_dict = manage_file.read_json_as_dict(track_result_file)

    count = 1
    for sentence in processed_lines:
        names = find_name.kakao_log_to_nouns(sentence[2])  # 내용에서 명사 찾기 (띄어쓰기, 명사, 조사)
        for name in names:
            if not except_string.except_string(name):  # 제외 : 3글자 미만, 숫자, 숫자+단위, 블랙리스트, 검색기록 있음
                results = naver_local.check_name(name, name)  # 네이버 지도 검색해서 1순위 or 2순위 있으면 return
                if results == -1:
                    print("네이버 지역 검색 API 할당량을 초과했습니다")
                    return
                elif results != []:
                    result_dict[name] = results  # 검색결과 추가

                    count += 1

                    if count % 10 == 0:
                        # 결과 중간 저장
                        manage_file.save_list_as_file(already_file, except_string.get_already_list())
                        manage_file.save_dict_as_json(track_result_file, result_dict)
                        print("count : " + str(count), end=" -> ")

                        t_time = time.time() - t_time
                        print('{:02d}:{:02d}'.format(int(t_time % 3600 // 60), int(t_time % 60)))

    manage_file.save_list_as_file(already_file, except_string.get_already_list())
    manage_file.save_dict_as_json(track_result_file, result_dict)
    print("검색 완료")
    return processed_lines, result_dict


def grade_question():
    processed_lines = preprocessing.preprocessing(kakao_file)  # [ [시간1, 이름1, 내용1], [시간2, 이름2, 내용2], ... ]

    score_result = []
    for time, name, sentence in processed_lines:
        score, tokens = is_question.grade(sentence)
        score_result.append([score, sentence, tokens])
    score_result.sort(key=lambda x: x[0])
    with open(grade_result_file, 'w') as file:
        for score, sentence, tokens in score_result:
            file.write(str(score) + " : ")
            file.write("{0:100}".format(sentence))
            file.write("// ")
            for token in tokens:
                file.write(token + " ")
            file.write('\n')

def split_with(pivot, sentences):
    # pivot 기준으로 문장 나누기

    new_sentences = []
    for sentence in sentences:
        if sentence.count(pivot) > 0:
            splited = sentence.split(pivot)
            for split in splited[:-1]:
                if len(split) > 0:
                    new_sentences.append(split + pivot)
            new_sentences.append(splited[-1])
        else:
            new_sentences.append(sentence)

    return_list = []
    for sentence in new_sentences:
        if sentence != "":
            return_list.append(sentence.strip())
    return return_list


def find_match():
    processed_lines, restaurant_dict = track_name()  # kakao_file에서 식당명 찾기
    restaurant_list = restaurant_dict.keys()  # 검색된 식당명 목록

    match_list = []
    count = 1
    finish_count = len(processed_lines)

    for time, name, sentence in processed_lines:

        # pivot 기준으로 문장 나누기
        sentences = [sentence]
        pivots = ["?", "!"]
        for pivot in pivots:
            sentences = split_with(pivot, sentences)

        for sentence in sentences:
            # 나눠진 문장에 대해서

            # 답변 찾기
            names = find_name.kakao_log_to_nouns(sentence)
            if sentence.count("샵검색") > 0:
                tmp_sentence = sentence.split("샵검색: #")[-1]
                if len(tmp_sentence.split()) > 1:
                    names.append(tmp_sentence.replace(" ", ""))

            # names = ["합정에", "괜찮은", "참치집", "있을까요", "있다"]

            check = 1
            restaurants = []
            for name in names:
                if name in restaurant_list:
                    # 식당명이 문장에 있으면

                    location = ""
                    if tmp_location in sentence:
                        # 지역명이 문장에 있으면
                        location = tmp_location

                    restaurants = restaurant_dict[name]

                    if len(results[0]) > 0:
                        # station_find 수정 필요
                        match = station_find(0, location, name, sentence, restaurants)
                        match_list.append({"sentence" : sentence, "QAN" : "A", "location" : location, "restaurant" : match})
                        check = 0

                    elif len(results[1]) > 0:
                        match = station_find(1, location, name, sentence, restaurants)
                        match_list.append({"sentence" : sentence, "QAN" : "A", "location" : location, "restaurant" : match})
                        check = 0

            if check == 1:
                # 이 문장이 답변이 아니었으면

                # 질문 찾기
                score, tokens = is_question.grade(sentence)
                category, location = find_inform(sentence)  # find_inform는 세연 제작 중
                if 0.65 <= score:
                    # 확정
                    match_list.append({"sentence" : sentence, "QAN" : "Q", "location" : location, "category" : category})
                    check = 0
                elif 0.55 <= score < 0.65:
                    # 확인이 필요한 문장
                    match_list.append({"sentence" : sentence, "QAN" : "QN", "location" : location, "category" : category})
                    check = 0
                elif score < 0.55:
                    # 점수 미달
                    pass

            if check == 1:
                # 이 문장이 답변도 질문도 아니었으면
                match_list.append({"sentence" : sentence, "QAN" : "N"})

        # 진행 출력
        if count % 100 == 0 or count % finish_count == 0:
            print("{0:5} / {1:5}".format(count, finish_count))
        count += 1

    # 결과 출력
    manage_file.save_list_as_file(match_result_file, match_list)


def station_find(score_number, station_name, name, sentence, results):
    if station_name == "":
        return
    if station_name in sentence:
        anothername = station_name + " " + name
        station_result = naver_local.check_name(anothername, name)
        namelist = []
        matchs_list = []
        for i in range(0, len(results)):
            for j in range(0, len(results[i])):
                namelist.append(results[i][j]['title'])

        if station_result == []:
            # 넘어가고 원래 결과 그대로 사용
            matchs_list = (['A', sentence, results[score_number][0]['title']])
        else:
            for i in range(0, len(station_result)):
                for j in range(0, len(station_result[i])):
                    if station_result[i][j]['title'] in namelist:
                        matchs_list = (['A', sentence, station_result[i][j]['title']])
                    else:
                        pass
    else:
        matchs_list = (['A', sentence, results[score_number][0]['title']])
    return matchs_list


if __name__ == "__main__":
    if args.track:
        track_name()
    elif args.grade:
        grade_question()
    elif args.match:
        find_match()
