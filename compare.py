import re
from sources import datas, manage_file

hangul = re.compile("[^ !?0-9가-힣]+")

question_list = manage_file.read_file_as_list("./datas/samples/kakao_questions.txt")

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

word_list = []
for question in question_list:

    # 기호(!?), 한글, 숫자만 남기기
    question = hangul.sub(" ", question)

    # 단어 치환
    for place in datas.place_list:
        question = question.replace(place, " 지역 ")
    for restaurant in datas.restaurant_list:
        question = question.replace(restaurant, " 이름 ")
    for food in datas.food_list:
        question = question.replace(food, " 음식 ")
    question = question.replace('!', ' ! ')
    question = question.replace('?', ' ? ')

    # pivot 기준으로 문장 나누기
    sentences = [question]
    pivots = ["?", "!"]
    for pivot in pivots:
        sentences = split_with(pivot, sentences)

    for sentence in sentences:
        word_list.extend(sentence.split())

result_list = []
for word in word_list:
    result_list.append((word, word_list.count(word)))

result_list = list(set(result_list))
for i in range(len(result_list)):
    result_list[i] = [result_list[i][0], result_list[i][1]]

result_list.sort(key=lambda x: x[1], reverse=True)

with open("./datas/samples/questions_after.txt", 'w') as file:
    for result in result_list:
        file.write(result[0] + ", " + str(result[1]) + "\n")