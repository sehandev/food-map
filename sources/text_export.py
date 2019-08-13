import pandas as pd

def question_data(question_data):
    question_user_data = []
    for i in range(len(0, question_data)):
        parse = qusetion_data[i]
        question_user_data.append(parse)

    question_user_data.sort(key=lambda x: x[0])
    name = question_user_data[0][0]
    for i in range(1, len(user_data)):  # 중복된 이름이면 지워주고 넘기는 것
        if name in question_user_data[i][0]:
            question_user_data[i][0] = question_user_data[i][0].replace(name, "")
        else:
            name = question_user_data[i][0]
    text_export(Q, question_user_data)
    
def answer_data(text_name):
    answer_user_data = []
    for i in range(len(0, question_data)):
        parse = answer_data[i]
        answer_user_data.append(parse)

    answer_user_data.sort(key=lambda x: x[0])
    name = answer_user_data[0][0]
    for i in range(1, len(user_data)):  # 중복된 이름이면 지워주고 넘기는 것
        if name in answer_user_data[i][0]:
            answer_user_data[i][0] = answer_user_data[i][0].replace(name, "")
        else:
            name = answer_user_data[i][0]
    text_export(A, answer_user_data)


def text_export(QNA, user_data):
    data = pd.DataFrame(user_data)
    data.columns = ['이름', '시간', '내용']
    data = data.set_index("이름")

    if QNA == "Q":
        data.to_csv('../datas/ADE_question_users', encoding='euc-kr')
    elif QNA == "A":
        data.to_csv('../datas/ADE_answer_users', encoding='euc-kr')


if __name__ == '__main__':
    question_data(질문데이터)
    answer_data(답변데이터)

