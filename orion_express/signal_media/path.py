from configparser import ConfigParser
import os

script_directory = os.path.abspath(os.path.dirname(__file__))

ini_path = os.path.join(script_directory, 'setting.ini')

parser = ConfigParser()
parser.read(ini_path)


def get_config_path(section, key):
    return os.path.join(script_directory, parser.get(section, key).replace("\\", os.path.sep))


path_before = os.path.join('signal_media', 'temp', 'input', '')
path_after_rename = os.path.join('signal_media', 'temp', 'schedule', '')
path_to_out = os.path.join('signal_media', 'temp', 'outter', '')
plst_dir = os.path.join('signal_media','temp',  'schedule', '')
dir_for_blocks = os.path.join('signal_media', 'temp', 'dir_for_blocks', '')
dir_input_playlist = os.path.join('signal_media', 'temp', 'input', '')
video_file = os.path.join('signal_media', 'old_new_sarafan.xlsx')
path_to_log = os.path.join('signal_media', 'temp', 'log')

# Пути к серверам
hd_out_osn = get_config_path('path', 'hd_out_osn')
hd_out_reserve = get_config_path('path', 'hd_out_reserve')
sd_out_osn = get_config_path('path', 'sd_out_osn')
sd_out_reserve = get_config_path('path', 'sd_out_reserve')
test_path = get_config_path('path', 'path_test')
