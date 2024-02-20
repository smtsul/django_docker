import csv
import json
import datetime
def check_sec_to_min(path,filename):
    result = ''  # Результат, который мы будем возвращать
    liner, g, timer = [], [], []

    with open(path + filename, newline='') as file:
        playlist = csv.reader(file, delimiter=';')
        for row in playlist:
            liner.append(row)

    for i in range(0, len(liner)):
        if len(liner[i]) != 0:
            temp = datetime.strptime(liner[i][0], '%H:%M:%S')
            timer.append(temp.minute * 60 + temp.hour * 60 * 60 + temp.second)
        else:
            timer.append('')

    for i in range(0, len(timer) - 4):
        if type(timer[i + 1]) == str:
            if 0 < timer[i + 2] - timer[i] < 180:
                if result == '':
                    result += 'В плейлисте:' + filename + ' проверь строки ' + str(i + 1) + '-' + str(i + 3) + ';'

    if len(result) < 3:
        result = {'error': False, 'message': 'В плейлисте:' + filename + ' ошибок нет'}
    else:
        result = {'error': True, 'message': result}

    return json.dumps(result, ensure_ascii=False)
