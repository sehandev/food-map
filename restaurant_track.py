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
# kakao_file = "./datas/ADE_test_2.txt"
kakao_file = "./datas/ADE_test_3.txt"
already_file = "./datas/already_list.txt"
track_result_file = "./results/restaurant.json"
grade_result_file = "./results/grade.txt"
match_result_file = "./results/match.txt"


def track_name():
    t_time = time.time()  # 시작 시간

    processed_lines = preprocessing.preprocessing(kakao_file)  # [ [시간1, 이름1, 내용1], [시간2, 이름2, 내용2], ... ]
    result_dict = manage_file.read_json_as_dict(track_result_file)

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
                    result_dict[name] = results

                    count += 1

                    if count % 10 == 0:
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

def find_match():
    print("trace_name function")
    processed_lines, restaurant_dict = track_name()
    restaurant_list = restaurant_dict.keys()

    match_list = []
    count = 1
    finish_count = len(processed_lines)

    for time, name, sentence in processed_lines:
        # 질문 찾기
        score, tokens = is_question.grade(sentence)
        if 0.65 <= score:
            # 자동 선택
            match_list.append(['QQ', sentence, score])
        elif 0.55 <= score < 0.65:
            # 수동 선택
            match_list.append(['Q', sentence, score])
        elif score < 0.55:
            # 점수 미달

            # 답변 찾기
            names = find_name.kakao_log_to_nouns(sentence)
            if sentence.count("샵검색") > 0:
                names.append(sentence.split("샵검색: #")[-1].replace(" ", ""))

            # names = ["합정에", "괜찮은", "참치집", "있을까요", "있다"]

            not_answer = 1
            for name in names:
                if name in restaurant_list:
                    results = restaurant_dict[name]
                else:
                    results = []

                if results != []:
                    if len(results[0]) > 0:
                        matchs_list = station_find(0, "공덕", name, sentence, results)
                        match_list.append(matchs_list)
                        not_answer = 0                    
                        
                    elif len(results[1]) > 0:
                        matchs_list = station_find(1, "공덕", name, sentence, results)
                        print(matchs_list)
                        print("?")
                        match_list.append(matchs_list)
                        not_answer = 0
                    else:
                        # 유사 결과만 있음
                        pass
            if not_answer:
                match_list.append(['N', sentence])

        # 진행 출력
        if count % 100 == 0:
            print("{0:5} / {1:5}".format(count, finish_count))
        count += 1

    # 결과 출력
    manage_file.save_list_as_file(match_result_file, match_list)


def station_find(score_number, station_name, name, sentence, results):
    if station_name in sentence :
        anothername = station_name + " " + name 
        print(anothername)
        station_result = naver_local.check_name(anothername)
        namelist = []
        matchs_list = []
        for i in range(0, len(results[0])):
            namelist.append(results[0][i]['title'])
        
        print("여기가 station_result")
        print(station_result)
        if station_result == []:
            # 넘어가고 원래 결과 그대로 사용
            matchs_list = (['A', sentence, results[score_number][0]['title']])
        else:
            if len(station_result[0]) > 0:
                if station_result[0][0]['title'] in namelist:
                    matchs_list = (['A', sentence, station_result[score_number][0]['title']]) 
                    print(matchs_list)    
                else: pass
            else: pass
    else :
        matchs_list = (['A', sentence, results[score_number][0]['title']])
    return matchs_list
    

if __name__ == "__main__":
    if args.track:
        track_name()
    elif args.grade:
        grade_question()
    elif args.match:
        find_match()