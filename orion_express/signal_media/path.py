from configparser import ConfigParser
import os

script_directory = os.path.abspath(os.path.dirname(__file__))

ini_path = os.path.join(script_directory, 'setting.ini')

parser = ConfigParser()
parser.read(ini_path)


def get_config_path(section, key):
    return os.path.join(script_directory, parser.get(section, key).replace("\\", os.path.sep))


# Пути из файла конфигурации
# path_before = get_config_path('path', 'path_before')
# path_after_rename = get_config_path('path', 'path_after_rename')
# path_kzpl_exe = get_config_path('path', 'path_kzpl_exe')
# path_after_kzpl = get_config_path('path', 'path_after_kzpl')
# plst_dir = get_config_path('path', 'plst_dir')
# dir_for_blocks = get_config_path('path', 'path_for_blocks')
# dir_input_playlist = get_config_path('path', 'path_before')
# video_file = get_config_path('path', 'video_file')
# path_to_out = get_config_path('path', 'path_out')
# dir_for_log = get_config_path('path', 'path_to_log')

'''Отказался от setting.ini так как пути в  линуксе пути работают через другой обратный слеш не работают'''

path_before = os.path.join('signal_media', 'temp', 'input', '')
path_after_rename = os.path.join('signal_media', 'temp', 'schedule', '')
path_after_kzpl = os.path.join('signal_media','temp', 'outter', '')
plst_dir = os.path.join('signal_media','temp',  'schedule', '')
dir_for_blocks = os.path.join('signal_media', 'temp', 'dir_for_blocks', '')
dir_input_playlist = os.path.join('signal_media', 'temp', 'input', '')
video_file = os.path.join('signal_media', 'old_new_sarafan.xlsx')
path_to_out = os.path.join('signal_media', 'temp', 'outter')
path_to_log = os.path.join('signal_media', 'temp', 'log')

# Пути к серверам
hd_out_osn = get_config_path('path', 'hd_out_osn')
hd_out_reserve = get_config_path('path', 'hd_out_reserve')
sd_out_osn = get_config_path('path', 'sd_out_osn')
sd_out_reserve = get_config_path('path', 'sd_out_reserve')
test_path = get_config_path('path', 'path_test')
