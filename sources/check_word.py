from collections import Counter

def get_tags(text, ntags=50):
    count = Counter(text)
    n_count_list = []
    p = 0
    for n, c in count.most_common(ntags):
        temp = {'tag': n, 'count': c }
        n_count_list.append(temp)
    return n_count_list


def combine_tag(word):
    if word == '?' or word == '??' or word == '...?' or word == '?!' or word == '!?':
        word = "질문"
    return word

def text_export(tags, all_word):
    result_file = open("../datas/log_standard_result.txt", 'w', -1, "utf-8-sig")
    for tag in tags:
        noun = tag['tag']
        count = tag['count']
        percent = round(100 * float(count) / float(all_word), 2)

        result_file.write('{} {}%\n'.format(noun, percent))
    result_file.close()

def main():
    noun_count = 500 # 숫자 임의로? 상위만 체크하니까 필요없을 것
    all_word = 0
    text_file = open("../datas/log_standard.txt", 'r', encoding='utf-8-sig')
    text = text_file.read().split()
    for i in range(len(text)):
        text[i] = combine_tag(text[i])
        all_word += 1

    tags = get_tags(text, noun_count)
    text_file.close()
    text_export(tags, all_word)

if __name__ == '__main__':
    main()
