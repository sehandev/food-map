import pandas as pd

#파일 송출

def question_data(question_data_list):  #질문 데이터 처리
    question_user_data = []
    for i in range(0, len(question_data_list)):
        parse = question_data_list[i]
        if question_data_list[i][2] != question_data_list[i-1][2]:  # question_data_list의 내용이 이전의 내용과 다를 경우에만 append
            question_user_data.append(parse)
        
    question_user_data.sort(key=lambda x: x[0])  # append한 데이터에 대해서 이름 기준으로 정렬
    name = question_user_data[0][0]
    for i in range(1, len(question_user_data)):  # 중복된 이름이면 지워주고 넘기는 것(가독성을 위해. 추후 이름이 함께 넘어와야할 때 for 지우면 됨)
        if name in question_user_data[i][0]:
            question_user_data[i][0] = question_user_data[i][0].replace(name, "")
        else:
            name = question_user_data[i][0]
    text_export("Q", question_user_data)  #Q 

def answer_data(answer_data_list):
    answer_user_data = []
    for i in range(0, len(answer_data_list)):
        parse = answer_data_list[i]
        if answer_data_list[i][2] != answer_data_list[i-1][2]:  # answer_data_list의 내용이 이전 내용과 다를 경우에만 append
            answer_user_data.append(parse)
    
    answer_user_data.sort(key=lambda x: x[0])  # append한 데이터에 대해서 이름 기준 정렬
    print(answer_user_data)
    name = answer_user_data[0][0]
    for i in range(1, len(answer_user_data)):  # 중복된 이름이면 지워주고 넘기는 것
        if name in answer_user_data[i][0]:
            answer_user_data[i][0] = answer_user_data[i][0].replace(name, "")
        else:
            name = answer_user_data[i][0]
    text_export("A", answer_user_data)


def text_export(QNA, user_data):
    data = pd.DataFrame(user_data)
    data.columns = ['이름', '시간', '내용']  # 이름=시간-내용 순으로 정렬
    data = data.set_index("이름")  # index num이후 데이터가 오는 파일형식 방지를 위해 이름을 index로 설정

    if QNA == "Q":
        writer = pd.ExcelWriter('./results/ADE_question_users.xlsx', engine='xlsxwriter') # Q일경우 question user file에 excel로 저장
    elif QNA == "A":
        writer = pd.ExcelWriter('./results/ADE_answer_users.xlsx', engine='xlsxwriter')  # A일경우 answer user file에 excel로 저장

    data.to_excel(writer, sheet_name='Sheet1')
    writer.save()


if __name__ == '__main__':
    question_data(question_data)
    answer_data(answer_data)