from operator import itemgetter

def text_compare():
    question_list = [['아시는분',13],['질문',20],['?', 10], ['넹',5]]
    not_question_list = [['안녕하세요',10], ['질문',10], ['?',5],['넹',30]]
    compare_list = []

    for i in range(len(question_list)) :
        for j in range(len(question_list)) :
            if question_list[i][0] == not_question_list[j][0]:
                percent = question_list[i][1] - not_question_list[j][1]
                word_percent = [question_list[i][0], percent]
                compare_list.append(word_percent)

    compare_list.sort(key=itemgetter(1))
    print(compare_list)

def main():
    text_compare()

if __name__ == '__main__':
    main()
