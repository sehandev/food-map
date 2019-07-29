from sources import preprocessing, find_name, except_string, naver_local, manage_file, is_question
import time
import signal
import pathlib
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--track", help="tracking rastaurant name", action="store_true")
parser.add_argument("--grade", help="grading questions", action="store_true")
args = parser.parse_args()


kakao_file = "./datas/kakao.txt"
already_file = "./datas/already_list.txt"
track_result_file = "./results/result.json"
grade_result_file = "./results/grade.txt"
question_file = "./datas/samples/kakao_questions_2.txt"


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
                    result_dict[name] = {"first": results[0], "second": results[1], "third": results[2]}

                    count += 1

                    if count % 10 == 0:
                        manage_file.save_list_as_file(already_file, except_string.get_already_list())
                        manage_file.save_dict_as_json(track_result_file, result_dict)
                        print("count : " + str(count), end=" -> ")

                        t_time = time.time() - t_time
                        print('{:02d}:{:02d}'.format(int(t_time % 3600 // 60), int(t_time % 60)))

    manage_file.save_list_as_file(already_file, except_string.get_already_list())
    print("검색 완료")


def grade_question():
    # processed_lines = preprocessing.preprocessing(kakao_file)  # [ [시간1, 이름1, 내용1], [시간2, 이름2, 내용2], ... ]
    processed_lines = preprocessing.preprocessing(question_file)  # [ [시간1, 이름1, 내용1], [시간2, 이름2, 내용2], ... ]

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


if __name__ == "__main__":
    if args.track:
        track_name()
    elif args.grade:
        grade_question()
