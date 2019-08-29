from sources import preprocessing, find_noun, except_string, naver_local, is_question, find_inform, answer_check, category_regularation, crawling_place, text_export, datas, find_tag
import time
import signal
import pathlib
import json
import argparse

# 원하는 기능을 실행하기 위한 parameter 설정
parser = argparse.ArgumentParser()
parser.add_argument("--track", help="tracking restaurant name", action="store_true")
parser.add_argument("--grade", help="grading questions", action="store_true")
parser.add_argument("--match", help="find match of question and answer", action="store_true")
args = parser.parse_args()



def time_report(message, t_time):
    # message와 함께 진행시간 출력

    print(message)
    t_time = int(time.time() - t_time)
    print('{:02d}:{:02d}\n'.format((t_time % 3600) // 60, t_time % 60))


def track_name():
    # kakao_file에서 식당명 찾기

    t_time = int(time.time())  # 시작 시간

    processed_lines = preprocessing.preprocessing()  # [ [시간1, 이름1, 내용1], [시간2, 이름2, 내용2], ... ]

    count = 1
    finish_count = len(processed_lines)
    for sentence in processed_lines:
        nouns = find_noun.kakao_log_to_nouns(sentence[2])  # 내용에서 명사 찾기 (띄어쓰기, 명사, 조사)
        for noun in nouns:
            if not except_string.except_string(noun):  # 제외 : 3글자 미만, 숫자, 숫자+단위, 블랙리스트, 검색기록 있음
                results = naver_local.check_name(noun, noun)  # 네이버 지도 검색해서 1순위 or 2순위 있으면 return
                if results == -1:
                    # error
                    print("네이버 지역 검색 API 할당량을 초과했습니다")
                    return -1, {}
                elif results != []:
                    # 정상
                    datas.restaurant_dict[noun] = results  # 검색결과 추가

        if count % 100 == 0:
            # 결과 중간 저장
            datas.save_already()
            datas.save_restaurant()
            print("count : " + str(count) + " / " + str(finish_count), end=" -> ")
            new_time = int(time.time() - t_time)
            print('{:02d}:{:02d}'.format((new_time % 3600) // 60, new_time % 60))
        count += 1

    # 정상 완료 : 결과 저장
    datas.save_already()
    datas.save_restaurant()

    datas.update()

    time_report("식당명 검색 완료", t_time)

    return processed_lines


def grade_question():
    # 문장이 질문일 확률을 점수화

    processed_lines = preprocessing.preprocessing()  # [ [시간1, 이름1, 내용1], [시간2, 이름2, 내용2], ... ]

    score_result = []
    for time_log, name, sentence in processed_lines:
        score, tokens = is_question.grade(sentence)
        score_result.append([score, sentence, tokens])
    score_result.sort(key=lambda x: x[0], reverse=True)

    datas.save_grade(score_result)


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

    # 공백 제거
    return_list = []
    for sentence in new_sentences:
        if sentence != "":
            return_list.append(sentence.strip())

    return return_list


def find_match():
    # A를 기준으로 Q match

    print("식당 검색")
    processed_lines = track_name()  # kakao_file에서 식당명 찾기

    if processed_lines == -1:
        # error
        return

    match_list = []  # match된 QA
    count = 1
    finish_count = len(processed_lines)

    t_time = int(time.time())  # 시작 시간
    print("QAN 확인 시작")

    for time_log, name, p_sentence in processed_lines:

        # pivot 기준으로 문장 나누기
        sentences = [p_sentence]
        pivots = ["?", "!"]
        for pivot in pivots:
            sentences = split_with(pivot, sentences)

        for sentence in sentences:
            # 나눠진 문장에 대해서

            # 답변 찾기
            nouns = find_noun.kakao_log_to_nouns(sentence)
            if sentence.count("샵검색") > 0:
                tmp_sentence = sentence.split("샵검색: #")[-1]
                if len(tmp_sentence.split()) > 1:
                    nouns.append(tmp_sentence.replace(" ", ""))

            # nouns = ["합정에", "괜찮은", "참치집", "있을까요", "있다"]

            check = 1
            places = []
            pre_restaurant = ""

            for noun in nouns:
                if noun in datas.place_list:
                    places.append(noun)

                if noun in datas.restaurant_list:
                    # 식당명이 문장에 있으면
                    if pre_restaurant == "":
                        # 첫 식당명이면
                        pre_restaurant = noun
                        check = 0
                    elif pre_restaurant != "":
                        # 이전에 식당명이 있었으면
                        match, location = answer_check.location_find(datas.restaurant_dict[pre_restaurant], pre_restaurant, places)
                        match_list.append({"name": name, "time": time_log, "sentence": sentence, "QAN": "A", "location": location, "title": pre_restaurant, "restaurant": match})

                        pre_restaurant = noun
                        if location != "":
                            places.remove(location)
                        check = 0

            if check == 0:
                # 식당명이 더 나오지 않아 추가되지 않은 식당명 처리
                match, location = answer_check.location_find(datas.restaurant_dict[pre_restaurant], pre_restaurant, places)
                match_list.append({"name": name, "time": time_log, "sentence": sentence, "QAN": "A", "location": location, "title": pre_restaurant, "restaurant": match})

            if check == 1:
                # 이 문장이 답변이 아니었으면

                # 질문 찾기
                score, tokens = is_question.grade(sentence)
                category, location = find_inform.find_inform(sentence)
                if 0.7 <= score:
                    # 확정
                    match_list.append({"name": name, "time": time_log, "sentence": sentence, "QAN": "Q", "location": location, "category": category})
                    check = 0
                elif 0.6 <= score < 0.7:
                    # 확인이 필요한 문장
                    match_list.append({"name": name, "time": time_log, "sentence": sentence, "QAN": "QN", "location": location, "category": category})
                    check = 0
                elif score < 0.6:
                    # 점수 미달
                    check = 1

            if check == 1:
                # 이 문장이 답변도 질문도 아니었으면
                match_list.append({"name": name, "time": time_log, "sentence": sentence, "QAN": "N"})

        # 진행 출력
        if count % 500 == 0 or count % finish_count == 0:
            print("{0:5} / {1:5}".format(count, finish_count))
        count += 1

    time_report("QAN 확인 완료", t_time)

    print("QA 매칭 시작")

    # QAN 확인 완료한 문장들 중 QA match 찾기
    match_result = []
    restaurant_data = []
    questioner_list = []
    answerer_list = []
    temp_question_tag_list = []
    temp_answer_tag_list = []

    finish_count = len(match_list)
    for i in range(finish_count):
        if match_list[i]["QAN"] == "A":  # A를 기준으로
            tmp_question_list = []  # match 후보
            for j in range(i - 5, i):  # 위로 5문장 확인
                if match_list[j]["QAN"] == "Q":  # Q가 있으면
                    # 지역 +2, 식당 순위 -1, 카테고리 +1, 순서 +0.1, 태그 +1
                    match_score = -3

                    match = match_list[i]["restaurant"]

                    location_score = 0  # 지역 점수
                    for location in match_list[j]["location"]:
                        if match_list[i]["location"] == location:
                            # Q와 A의 지역이 같으면
                            location_score = 2

                        match, _ = answer_check.location_find(match, match_list[i]["title"], location)  # 지역명과 함께 검색해서 우선순위 변경


                    for grade in range(3):
                        for restaurant in match[grade]:
                            a_category = category_regularation.find_category(restaurant["category"])
                            category_score = 0
                            tag_score = 0
                            for q_category in match_list[j]["category"]:
                                temp_question_tag_list = find_tag.tag_list(match_list[j]["sentence"], q_category)
                                for tags in temp_question_tag_list:
                                    tags = tags.replace("#", "").strip()
                                    if tags in match_list[i]["sentence"]:
                                        tag_score = tag_score + 1
                                if a_category == q_category:
                                    category_score = 1


                            new_score = location_score - grade + category_score + (j * 0.1) + tag_score
                            if match_score < new_score:
                                match_score = new_score
                                highest_restaurant = restaurant

                    tmp_question_list.append([match_score, highest_restaurant, j])

            if tmp_question_list != []:
                tmp_question_list.sort(key=lambda x: x[0])

                q = match_list[tmp_question_list[0][2]]
                a = match_list[i]

                recommend = tmp_question_list[0][1]
                title = recommend["title"]
                category = category_regularation.find_category(recommend["category"])
                address = recommend["address"]

                # 매칭 : [Q, A, 식당 정보]
                match_result.append([str(q["sentence"]), str(a["sentence"]), title, category])

                # 식당 정보 : [식당명, 카테고리, 질문+답변 문장]
                restaurant_data.append([title, category, q["sentence"] + " " + a["sentence"], address])

                # 유저 정보 : [이름, 시간, 내용]
                questioner_list.append([q["name"], q["time"], q["sentence"]])
                answerer_list.append([a["name"], a["time"], a["sentence"]])

        # 진행 출력
        if i > 0 and (i % 500 == 0 or i % finish_count == 0):
            print("{0:5} / {1:5}".format(i, finish_count))

    time_report("QA 매칭 완료", t_time)

    # 매칭 결과 출력
    datas.save_match(match_result)
    time_report("매칭 결과 출력", t_time)

    # 식당 정보 -> 식당명, 지번, 도로명, 카테고리, 영업시간, 태그
    text_export.place_export(restaurant_data)

    time_report("식당 정보 출력", t_time)

    # 유저 정보 -> 저장
    text_export.question_data(questioner_list)
    text_export.answer_data(answerer_list)

    time_report("유저 정보 출력", t_time)


if __name__ == "__main__":
    if args.track:
        track_name()
    elif args.grade:
        grade_question()
    elif args.match:
        find_match()
