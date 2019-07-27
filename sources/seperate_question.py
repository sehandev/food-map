with open("/home/sehan/git/food-map/datas/kakao_log.txt", 'r') as file:
    origin = file.read().split('\n')

with open("/home/sehan/git/food-map/datas/samples/kakao_questions_2_log.txt", 'r') as file:
    questions = file.read().split('\n')

new_list = []
for tmp in origin:
    check = 1
    for question in questions:
        if question in tmp:
            new_list.append(tmp.replace(question, "아마도질문"))
            check = 0
    if check == 1:
        new_list.append(tmp)



with open("/home/sehan/git/food-map/datas/kakao_log_left.txt", 'w') as file:
    for line in new_list:
        file.write(line + '\n')

