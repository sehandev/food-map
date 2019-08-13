from sources import preprocessing, find_name, except_string, naver_local, manage_file, is_question, find_inform, answer_check, category_regularation, crawling_place
import time
import signal
import pathlib
import json
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("--track", help="tracking restaurant name", action="store_true")
parser.add_argument("--grade", help="grading questions", action="store_true")
parser.add_argument("--match", help="find match of question and answer", action="store_true")
args = parser.parse_args()


# kakao_file = "./datas/kakao.txt"
kakao_file = "./datas/ADE_test_2.txt"
# kakao_file = "./datas/ADE_test_3.txt"
already_file = "./datas/already_list.txt"
place_file = "./datas/place_name.txt"

track_result_file = "./results/restaurant.json"
grade_result_file = "./results/grade.txt"
match_result_file = "./results/match_result.csv"


def track_name():
    # kakao_file에서 식당명 찾기
    t_time = time.time()  # 시작 시간

    processed_lines = preprocessing.preprocessing(kakao_file)  # [ [시간1, 이름1, 내용1], [시간2, 이름2, 내용2], ... ]
    result_dict = manage_file.read_json_as_dict(track_result_file)

    count = 1
    for sentence in processed_lines:
        nouns = find_name.kakao_log_to_nouns(sentence[2])  # 내용에서 명사 찾기 (띄어쓰기, 명사, 조사)
        for noun in nouns:
            if not except_string.except_string(noun):  # 제외 : 3글자 미만, 숫자, 숫자+단위, 블랙리스트, 검색기록 있음
                results = naver_local.check_name(noun, noun)  # 네이버 지도 검색해서 1순위 or 2순위 있으면 return
                if results == -1:
                    print("네이버 지역 검색 API 할당량을 초과했습니다")
                    return
                elif results != []:
                    result_dict[noun] = results  # 검색결과 추가

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

    place_list = manage_file.read_file_as_list(place_file)

    for time, name, sentence in processed_lines:

        # pivot 기준으로 문장 나누기
        sentences = [sentence]
        pivots = ["?", "!"]
        for pivot in pivots:
            sentences = split_with(pivot, sentences)

        for sentence in sentences:
            # 나눠진 문장에 대해서

            # 답변 찾기
            nouns = find_name.kakao_log_to_nouns(sentence)
            if sentence.count("샵검색") > 0:
                tmp_sentence = sentence.split("샵검색: #")[-1]
                if len(tmp_sentence.split()) > 1:
                    nouns.append(tmp_sentence.replace(" ", ""))

            # nouns = ["합정에", "괜찮은", "참치집", "있을까요", "있다"]

            check = 1
            places = []
            pre_restaurant= ""

            for noun in nouns:
                if noun in place_list:
                    places.append(noun)

                if noun in restaurant_list:
                    # 식당명이 문장에 있으면
                    if pre_restaurant == "":
                        # 첫 식당명이면
                        pre_restaurant = noun
                        check = 0
                    elif pre_restaurant != "":
                        # 이전에 식당명이 있었으면
                        match, location = answer_check.location_find(restaurant_dict[pre_restaurant], pre_restaurant, places)
                        match_list.append({"sentence" : sentence, "QAN" : "A", "location" : location, "name" : pre_restaurant, "restaurant" : match})

                        pre_restaurant = noun
                        if location != "":
                            places.remove(location)
                        check = 0

            if check == 0:
                # 식당명이 더 나오지 않아 추가되지 않은 식당명 처리
                match, location = answer_check.location_find(restaurant_dict[pre_restaurant], pre_restaurant, places)
                match_list.append({"sentence" : sentence, "QAN" : "A", "location" : location, "name" : pre_restaurant, "restaurant" : match})

            if check == 1:
                # 이 문장이 답변이 아니었으면

                # 질문 찾기
                score, tokens = is_question.grade(sentence)
                category, location = find_inform.find_inform(sentence)  # find_inform는 세연 제작 중
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
                    check = 1

            if check == 1:
                # 이 문장이 답변도 질문도 아니었으면
                match_list.append({"sentence" : sentence, "QAN" : "N"})

        # 진행 출력
        if count % 100 == 0 or count % finish_count == 0:
            print("{0:5} / {1:5}".format(count, finish_count))
        count += 1

    # QAN 확인 완료한 문장들 중 QA match 찾기
    match_result = []
    restaurant_data = []
    for i in range(len(match_list)):
        if match_list[i]["QAN"] == "A":
            tmp_question_list = []
            for j in range(i-10, i):
                if match_list[j]["QAN"] == "Q":
                    # 지역 +10, 식당 순위 -1, 카테고리 +1, 순서 +0.1
                    match_score = -3

                    match = match_list[i]["restaurant"]

                    location_score = 0
                    for location in match_list[j]["location"]:
                        if match_list[i]["location"] == location:
                            location_score = 2

                        match, _ = answer_check.location_find(match, match_list[i]["name"], location)

                    for grade in range(3):
                        for restaurant in match[grade]:
                            a_category = category_regularation.find_category(restaurant["category"])
                            category_score = 0
                            for q_category in match_list[j]["category"]:
                                if a_category == q_category:
                                    category_score = 1

                            new_score = location_score - grade + category_score + (j * 0.1)
                            if match_score < new_score:
                                match_score = new_score
                                highest_restaurant = restaurant

                    tmp_question_list.append([match_score, highest_restaurant, j])

            if tmp_question_list != []:
                tmp_question_list.sort(key=lambda x: x[0])

                q = str(match_list[tmp_question_list[0][2]]["sentence"])
                a = str(match_list[i]["sentence"])

                recommend = tmp_question_list[0][1]
                title = recommend["title"]
                category = category_regularation.find_category(recommend["category"])

                # 매칭 : [Q, A, 식당 정보]
                match_result.append([q, a, title, category])

                # 식당 정보 : [식당명, 카테고리, 질문+답변 문장]
                restaurant_data.append([title, category, q + " " + a])

    # 매칭 결과 출력
    with open(match_result_file, 'w', encoding='euc-kr') as file:
        writer = csv.writer(file)
        writer.writerows(match_result)
    # manage_file.save_list_as_file(match_result_file, match_result)

    # 식당 정보 -> 식당명, 지번, 도로명, 카테고리, 영업시간, 태그
    # crawling_place.set_data(restaurant_data)


if __name__ == "__main__":
    if args.track:
        track_name()
    elif args.grade:
        grade_question()
    elif args.match:
        find_match()
