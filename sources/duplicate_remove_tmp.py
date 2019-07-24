with open("/home/sehan/git/food-map/datas/except_list.txt", 'r') as file:
    lines = file.read().split('\n')
    lines = list(set(lines))

lines.sort(key=len)

with open("/home/sehan/git/food-map/datas/except_list_2.txt", 'w') as file:
    for line in lines:
        file.write(line + '\n')