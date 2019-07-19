from twkorean import TwitterKoreanProcessor
processor = TwitterKoreanProcessor(normalization=False, stemming=False)

with open("../datas/kakao_questions.txt", 'r') as file:
    lines = file.read().split('\n')
    lines = list(set(lines))

lines.sort(key=len)

with open("../datas/kakao_questions_dup_remove.txt", 'w') as file:
    for line in lines:
        tokens = processor.tokenize_to_strings(line)
        if len(tokens) <= 30:
            for token in tokens:
                file.write(token.replace("$$", '') + ' ')
            file.write('\n')
