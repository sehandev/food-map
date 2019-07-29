from operator import itemgetter

def text_compare(question_list, not_question_list):
    # question_list = [['아시는분',13],['질문',20],['?', 10], ['넹',5]]
    # not_question_list = [['안녕하세요',10], ['질문',10], ['?',5],['넹',30]]
    compare_list = []
    only_question_list = []

    for i in range(len(question_list)) :
        check = 0
        for j in range(len(not_question_list)) :
            if question_list[i][0] == not_question_list[j][0]:
                percent = question_list[i][1] - not_question_list[j][1]
                word_percent = [question_list[i][0], percent]
                compare_list.append(word_percent)
                check = 1

        if check == 0:
            word_percent = [question_list[i][0], question_list[i][1]]
            only_question_list.append(word_percent)

    compare_list.sort(key=itemgetter(1), reverse=True)
    only_question_list.sort(key=itemgetter(1), reverse=True)
        
    return compare_list, only_question_list


def main():
    text_compare(question, not_question)

if __name__ == '__main__':
    main()