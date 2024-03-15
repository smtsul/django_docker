from django.urls import path
from . import views

app_name = 'shot'

urlpatterns = [
    path('upload_files/', views.index, name='index'),]