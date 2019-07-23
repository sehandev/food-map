from sources import manage_file

def preprocessing(kakao_file):

    lines = manage_file.read_file_as_list(kakao_file)
    new_lines = []  # 새롭게 작성할 문서
    for line in lines[2:]:

        # 빈 줄 제거
        if line == "":
            continue

        # 2018년 8월 19일 일요일
        if 15 <= len(line) <= 18:
            if line[4] == "년" and line[-5] == "일" and line[-2:] == "요일":
                continue

        # 2018. 8. 22. 오후 8:20: sehan님이 들어왔습니다.
        if line[-7:] == "들어왔습니다.":
            continue

        # 2018. 9. 9. 오후 4:21: sehan님이 나갔습니다.
        if line[-6:] == "나갔습니다.":
            continue

        # 2018. 11. 1. 오후 6:39, sehan : 사진
        if line[-5:] == " : 사진":
            continue

        # 운영정책을 위반한 메시지로 신고 접수 시 카카오톡 이용에 제한이 있을 수 있습니다.
        if line == "운영정책을 위반한 메시지로 신고 접수 시 카카오톡 이용에 제한이 있을 수 있습니다.":
            continue

        # 삭제된 메시지입니다.
        if line == "삭제된 메시지입니다.":
            continue

        # 2018. 11. 1. 오후 6:39: 채팅방 관리자가 메시지를 가렸습니다.
        if line[-20:] == "채팅방 관리자가 메시지를 가렸습니다.":
            continue

        # 2018. 11. 1. 오후 6:39: sehan님을 내보냈습니다.
        if line[-10:] == "님을 내보냈습니다.":
            continue

        line = line.replace("이모티콘", '')

        time_name_log = line.split(',', maxsplit=1)

        # 2018. 8. 18. 오후 6:45, sehan : ㅎㅇ

        if len(time_name_log) > 1:
            time_name_log = [time_name_log[0]] + time_name_log[1].split(' : ', maxsplit=1)
            time_stamp = time_name_log[0]
            if len(time_stamp) >= 2:
                if len(time_stamp.split('.')) == 4:
                    tmp = time_stamp.split('.')[3][1:3]
                    if tmp == "오전" or tmp == "오후":
                        new_lines.append(time_name_log)
                        continue

        new_lines[-1][2] += " $$ " + line

    pre_name = new_lines[0][1]  # 동일인물이 여러 번 말하면 합치기 위한
    pre_index = 0
    processed_lines = [new_lines[0]]
    for i in range(1, len(new_lines)):
        if new_lines[i][2] != ' ':
            if new_lines[i][2][:7] == " 톡게시판 '":
                continue
            if pre_name == new_lines[i][1]:  # 이름이 같으면
                new_lines[pre_index][2] += " $$ " + new_lines[i][2]  # 내용 연결
            else:  # 이름이 다르면
                pre_name = new_lines[i][1]
                pre_index = i
                processed_lines.append(new_lines[i])

    with open(kakao_file[:-4] + "_processed.txt", 'w') as file:
        for line in processed_lines:
            file.write(line[0] + ',')
            file.write(line[1] + ' : ')
            file.write(line[2] + '\n')

    with open(kakao_file[:-4] + "_log.txt", 'w') as file:
        for line in processed_lines:
            file.write(line[2] + '\n')

    # with open(kakao_file[:-4] + "_processed_without_time.txt", 'w') as file:
    #     for line in processed_lines:
    #         file.write(line[1][1:] + ' : ')
    #         file.write(line[2] + '\n')

    # with open(kakao_file[:-4] + "_processed_only_question.txt", 'w') as file:
    #     for line in processed_lines:
    #         if line[2].count('?') > 0:
    #             file.write(line[2].strip() + '\n')
    #
    # with open(kakao_file[:-4] + "_processed_not_question.txt", 'w') as file:
    #     for line in processed_lines:
    #         if line[2].count('?') == 0 and line[2].count('!') == 0:
    #             file.write(line[2].strip() + '\n')
    #
    # with open(kakao_file[:-4] + "_processed_only_exclamation.txt", 'w') as file:
    #     for line in processed_lines:
    #         if line[2].count('!') > 0:
    #             file.write(line[2].strip() + '\n')

    return processed_lines
