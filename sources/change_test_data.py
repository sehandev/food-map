
test_file = "./datas/samples/ADE_test.txt"
result_file = "./datas/ADE_test_2.txt"

def process():
    with open(test_file, 'r') as file:
        lines = file.read().split('\n')

    processed_lines = []
    for line in lines:
        if line != "":
            processed_lines.append(line.split('] ')[-1])

    with open(result_file, 'w') as file:
        for i in range(len(processed_lines)):
            file.write("2019. 12. 31. 오후 12:31, sehan" + str(i) + " : " + processed_lines[i] + '\n')

process()