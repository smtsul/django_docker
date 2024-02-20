from django.urls import path
from . import views

app_name = 'signal_media'

urlpatterns = [
    path('upload_files/', views.upload_files, name='upload_files'),
    path('edit_setting/',views.edit_setting,name='edit_setting'),
    path('ajax_get_file_list/', views.ajax_get_file_list, name='ajax_get_file_list'),
    path('download_file/<str:file_name>/', views.download_file, name='download_file'),
    path('',views.index,name='index'),
    path('your_ajax_url/', views.your_ajax_view, name='your_ajax_url'),
    path('test_ajax_log/',views.test_ajax_log,name='test_ajax_log'),
    path('logged/',views.logged,name='logged'),
]