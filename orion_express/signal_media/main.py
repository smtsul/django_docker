import datetime
import os
import json
from django.http import JsonResponse
from .function import *


def create_time(year):
    play_list_dir = open_file(path_before)
    for i in range(0, len(play_list_dir)):
        rename_recopy(play_list_dir[i].split(), year)
    blocks = []
    plst_in = open_file(path_after_rename)
    info = []
    info_for_json = {'info': '',
                     'error': ''}
    for i in range(0, len(plst_in)):
        chanel_name = plst_in[i].split("_")[-1].split(".")[0]
        if chanel_name.lower() == 'нст':  # блядский костыль
            chanel_name = "НСТ"
        blocks, info_elem = parser_v2_test(path_after_rename, plst_in[i], chanel_name)
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
    plst_in = open_file(path_after_rename)
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
    my_list = open_file(path_to_out)
    success_count = 0
    failure_count = 0
    errors = []
    for file_name in my_list:
        result = copy_after_my_parser(file_name.split())
        if not result.get('error'):
            success_count += 1
        else:
            failure_count += 1
            errors.append(result['message'])
    return {'success_count': success_count, 'failure_count': failure_count, 'errors': errors}




def rename(year):
    my_list = []
    my_list = open_file(path_before)
    for i in range(0, len(my_list)):
        rename_recopy_v2(my_list[i].split('_'), year)
