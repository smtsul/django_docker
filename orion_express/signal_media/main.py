import datetime
import os
import json
from .function import *


def create_time(year):
    play_list_dir = open_file(dir_input_playlist)
    for i in range(0, len(play_list_dir)):
        rename_recopy(play_list_dir[i].split(), year)
    blocks = []
    plst_in = open_file(plst_dir)
    info = []
    info_for_json = {'info': '',
                     'error': ''}
    for i in range(0, len(plst_in)):
        chanel_name = plst_in[i].split("_")[-1].split(".")[0]
        if chanel_name.lower() == 'нст':  # блядский костыль
            chanel_name = "НСТ"
        blocks, info_elem = parser_v2_test(plst_dir, plst_in[i], chanel_name)
        info.append(info_elem)
        new_file_name = plst_in[i].replace("_", "-").replace(".xlsx", ".txt")
        if os.name == 'nt':
            new_file_name = '\\' + new_file_name[:4] + "-" + new_file_name[4:6] + '-' + new_file_name[
                                                                                        6:]  # Добавляем дефис между годом и месяцем for windows
        elif os.name == 'posix':
            new_file_name = '//' + new_file_name[:4] + "-" + new_file_name[4:6] + '-' + new_file_name[
                                                                                        6:]  # Добавляем дефис между годом и месяцем for unix
        # print(plst_in[i] + '  ' + new_file_name)
        write_list_to_file(blocks, dir_for_blocks + new_file_name)  # записываем временные блоки в файл
    return ' '.join(map(str, info))


def created_blocks():
    plst_in = open_file(plst_dir)
    for i in range(0, len(plst_in)):
        chanel_name = plst_in[i].split("_")[-1].split(".")[0]
        if chanel_name.lower() == 'нст':  # блядский костыль
            chanel_name = "НСТ"
        new_blocks = []
        new_file_name = plst_in[i].replace("_", "-").replace(".xlsx", ".txt")
        if os.name == 'nt':
            new_file_name = '\\' + new_file_name[:4] + "-" + new_file_name[4:6] + '-' + new_file_name[
                                                                                        6:]  # Добавляем дефис между годом и месяцем for windows
        elif os.name == 'posix':
            new_file_name = '//' + new_file_name[:4] + "-" + new_file_name[4:6] + '-' + new_file_name[
                                                                                        6:]  # Добавляем дефис между годом и месяцем for unix
        # new_file_name = '\\' + new_file_name[:4] + "-" + new_file_name[4:6] + '-' + new_file_name[6:]
        if os.name == 'nt':
            new_blocks = read_list_from_file(dir_for_blocks + '\\' + new_file_name)  # считываем
        elif os.name == 'posix':
            new_blocks = read_list_from_file(dir_for_blocks + '//' + new_file_name)  # считываем
        new_file_name = plst_in[i].replace(".xlsx", ".csv")
        new_file_name = new_file_name[:4] + "_" + new_file_name[4:]
        if 'сарафан' in chanel_name.lower():
            blocks_result = create_blocks_v4_sarafan(video_file, new_blocks, chanel_name)
        else:
            blocks_result = create_blocks_v4_rand(video_file, new_blocks, chanel_name)
        write_blocks_to_file(blocks_result, path_to_out, plst_in[i])


def copy_to_coder():
    try:
        my_list = open_file(path_to_out)
        count = 0
        for i in range(0, len(my_list)):
            copy_after_kzpl(my_list[i].split())
            count += 1
        plst_to_log()
        result = {
            "count": count
        }
        return json.dumps(result)
    except Exception as e:
        error_result = {
            "error": str(e)
        }
        return json.dumps(error_result)


def rename(year):
    my_list = []
    my_list = open_file(path_before)
    print(my_list)
    for i in range(0, len(my_list)):
        rename_recopy_v2(my_list[i].split('_'), year)

