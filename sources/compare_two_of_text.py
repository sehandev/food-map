from operator import itemgetter

def text_compare(question_list, not_question_list):  #질문에서 자주 등장하는 단어 빈도 percent로 측정하는 함수
    # question_list = [['아시는분',13],['질문',20],['?', 10], ['넹',5]]
    # not_question_list = [['안녕하세요',10], ['질문',10], ['?',5],['넹',30]]
    compare_list = []
    only_question_list = []

    for i in range(len(question_list)) :
        check = 0
        for j in range(len(not_question_list)) :
            if question_list[i][0] == not_question_list[j][0]: # question_list의 단어가 not_question_list의 단어에도 있으면
                percent = question_list[i][1] - not_question_list[j][1]  # 단어 빈도 percent 감소 ㅡ 비질문 데이터의 빈도
                word_percent = [question_list[i][0], percent]  # 단어-퍼센트 연결
                compare_list.append(word_percent)
                check = 1

        if check == 0:  # not_question_list에 없는데 question_list에는 있으면
            word_percent = [question_list[i][0], question_list[i][1]]  # percent 그대로 적용, 단어-퍼센트 연결
            only_question_list.append(word_percent)  # 추가

    compare_list.sort(key=itemgetter(1), reverse=True)  # sort
    only_question_list.sort(key=itemgetter(1), reverse=True)  #sort

    return compare_list, only_question_list


def main():
    text_compare(question, not_question)

if __name__ == '__main__':
    main()