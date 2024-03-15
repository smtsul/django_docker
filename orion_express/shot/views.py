from django.shortcuts import render
import os
from django.core.files.storage import FileSystemStorage
import os
from django.shortcuts import render

# Create your views here.


def index(reqiest):
    return render(reqiest, 'signal_media/base.html', )

def upload_files(request):
    files = []
    if request.method == 'POST':
        script_directory = os.path.abspath(os.path.dirname(__file__))
        input_folder = os.path.join(script_directory, "temp", "input")
        fs = FileSystemStorage(location=input_folder)
        for myfile in request.FILES.getlist('myfile'):
            # Удаляем существующий файл с тем же именем
            existing_file_path = fs.path(myfile.name)
            if fs.exists(existing_file_path):
                fs.delete(existing_file_path)
            fs.save(myfile.name, myfile)
        folder_path = os.path.join(script_directory, "temp", "outter")
        files = get_file_list(folder_path)
    return render(request, 'signal_media/upload.html', {'plst': files})