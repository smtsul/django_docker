from django.http import JsonResponse
from rest_framework.views import APIView
import os
from .main import copy_to_coder, check_sec, check_sec_to_min, plst_to_log, open_file, path_before, path_to_out, \
    path_after_rename, create_time, created_blocks
from .views import get_file_list


class signalka(APIView):
    @staticmethod
    def get(request):
        year = request.GET.get('year')
        code = request.GET.get('code')
        if year is not None:
            year = int(year)
        elif code is not None:
            code = int(code)
        try:
            results = []
            files = []
            if year is not None:
                create_time(year)
                created_blocks()
                script_directory = os.path.abspath(os.path.dirname(__file__))
                folder_path = os.path.join(script_directory, "temp", "outter")
                files = get_file_list(folder_path)
                if os.name == 'nt':
                    temp_path_out = path_to_out + '\\'
                    temp_path_input = path_after_rename + '\\'
                elif os.name == 'posix':
                    temp_path_out = path_to_out + '//'
                    temp_path_input = path_after_rename + '//'
                if request.method == 'GET':
                    result_min, result_sec = '', ''
                    plst_input = open_file(path_after_rename)
                    plst_output = open_file(path_to_out)
                    for i in range(0, len(plst_input)):
                        result_min = check_sec_to_min(temp_path_out, plst_output[i])
                        result_sec = check_sec(temp_path_out, plst_output[i], temp_path_input, plst_input[i])
                        results.append({'result_min': result_min, 'result_sec': result_sec})
            elif code == 1:
                results=[]
                #results.append(copy_to_coder())  # TODO включить, когда расшарят кодеры
                results.append(plst_to_log())
                return JsonResponse({'results': results})
            return JsonResponse({'results': results, 'files': files})
        except Exception as e:
            return JsonResponse({'error': True, 'msg': str(e)})