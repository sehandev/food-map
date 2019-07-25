with open("/home/sehan/git/food-map/datas/samples/kakao_questions.txt", 'r') as file:
    lines = file.read().split('\n')
    lines = list(set(lines))

lines.sort(key=len)

with open("/home/sehan/git/food-map/datas/samples/kakao_questions_2.txt", 'w') as file:
    for i in range(len(lines)):
        file.write("2018. 11. 29. 오후 1:14, 옹" + str(i) + " : " + lines[i] + '\n')