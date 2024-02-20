from .main import create_time, created_blocks
from .main import copy_to_coder,check_sec,check_sec_to_min, plst_to_log,open_file,path_before,path_to_out,path_after_rename #for testing
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
import os
from django.shortcuts import render
from .forms import SettingForm
from django.http import FileResponse, Http404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt  # костылек
def your_ajax_view(request):
    if request.method == 'POST':
        year = request.POST.get('year')
        create_time(year)
        created_blocks()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def your_ajax_view(request):
    if request.method == 'POST':
        # Извлекаем данные из запроса
        year = request.POST.get('year')
        # Вызываем функцию rename с переданным годом
        create_time(year)
        created_blocks()
        # plst_to_log()
        # Возвращаем JSON-ответ (это необязательно, зависит от вашего случая)
        return JsonResponse({'status': 'success'})

    # Обработка других случаев (например, GET-запросов)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def index(reqiest):
    return render(reqiest, 'signal_media/base.html', )


def download_file(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'temp', 'outter', file_name)
    # file_path=os.path.join(path_before,file_name)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'))
        return response
    else:
        raise Http404("File not found")


def get_file_list(folder_path):
    try:
        files = os.listdir(folder_path)
        return files
    except OSError as e:
        print(f"Error reading files from {folder_path}: {e}")
        return []


def ajax_get_file_list(request):
    script_directory = os.path.abspath(os.path.dirname(__file__))
    folder_path = os.path.join(script_directory, "temp", "outter")
    files = get_file_list(folder_path)
    return JsonResponse({'files': files})


def upload_files(request):
    files = []
    if request.method == 'POST':
        script_directory = os.path.abspath(os.path.dirname(__file__))
        input_folder = os.path.join(script_directory, "temp", "input")
        # input_folder=os.path.join(script_directory,path_before)
        fs = FileSystemStorage(location=input_folder)
        for myfile in request.FILES.getlist('myfile'):
            # Удаляем существующий файл с тем же именем
            existing_file_path = fs.path(myfile.name)
            if fs.exists(existing_file_path):
                fs.delete(existing_file_path)
            # Сохраняем новый файл
            fs.save(myfile.name, myfile)
            # rename(2023)
            # create_time()
            # created_blocks()
        folder_path = os.path.join(script_directory, "temp", "outter")
        # folder_path = os.path.join(script_directory,path_to_out)
        files = get_file_list(folder_path)
    return render(request, 'signal_media/upload.html', {'plst': files})


def edit_setting(request):  # редактирование настроек для обработки плейлистов
    script_directory = os.path.abspath(os.path.dirname(__file__))
    ini_path = os.path.join(script_directory, "setting.ini")
    with open(ini_path, 'r', encoding='UTF-8') as f:
        setting_content = f.read()
    if request.method == 'POST':
        # Обработка отправки формы
        form = SettingForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data['setting_content']
            # Запись нового содержимого обратно в setting.ini
            with open(ini_path, 'w', encoding='UTF-8') as f:
                f.write(new_content)
    else:
        form = SettingForm(initial={'setting_content': setting_content})
    return render(request, 'signal_media/edit_setting.html', {'form': form})


def test_ajax_log(request):  # TODO доделать логи, вывод в json
    # plst_to_log()
    if os.name == 'nt':
        temp_path_out = path_to_out + '\\'
        temp_path_input=path_after_rename+'\\'
    elif os.name == 'posix':
        temp_path_out = path_to_out + '//'
        temp_path_input = path_after_rename + '//'
    if request.method == 'GET':
        # try:
        # Вызываем plst_to_log
        result_min,result_sec='',''
        plst_input=open_file(path_after_rename)
        plst_output=open_file(path_to_out)
        results = []
        for i in range(0, len(plst_input)):
            result_min = check_sec_to_min(temp_path_out, plst_output[i])
            #result_sec = check_sec(temp_path_out, plst_output[i], temp_path_input, plst_input[i])
            results.append({'result_min': result_min, 'result_sec': result_sec})
        #print('results:', results)
        #plst_to_log()
        return JsonResponse({'results': results})
        # except Exception as e:
        #     # return JsonResponse({'error': True, 'message': str(e)})
        #     print(e)
    return JsonResponse({'error': True, 'message': 'Invalid request method'})


def logged(request):
    # TODO: выполните необходимые действия
    result=plst_to_log()
    return JsonResponse(result)