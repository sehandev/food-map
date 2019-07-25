from collections import Counter


def get_tags(text, ntags=50):
    count = Counter(text)
    n_count_list = []
    p = 0
    for n, c in count.most_common(ntags):
        n_count_list.append([n, c])
    return n_count_list


def combine_tag(word):
    if word.count('!') + word.count('?') > 0:
        return '?'
    return word


def text_export(tags):
    result_file = open("../datas/standard_result.txt", 'w', -1, "utf-8-sig")
    for tag in tags:
        noun = tag[0]
        percent = tag[1]

        result_file.write('{},{}\n'.format(noun, percent))
    result_file.close()


def count_words(text):
    noun_count = 500  # 숫자 임의로? 상위만 체크하니까 필요없을 것
    all_word = len(text)

    for i in range(all_word):
        text[i] = combine_tag(text[i])

    n_count_list = get_tags(text, noun_count)

    for i in range(len(n_count_list)):
        n_count_list[i][1] = round(100 * float(n_count_list[i][1]) / float(all_word), 2)

    return n_count_list


if __name__ == '__main__':
    text_file = open("../datas/questions_stadard.txt", 'r', encoding='utf-8-sig')
    text = text_file.read().split()
    tags = count_words(text)
    text_file.close()
    text_export(tags)
