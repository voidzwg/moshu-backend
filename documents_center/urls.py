from django.urls import path
from .views import *

urlpatterns = [
    path('',documents_center),
    path('open_file/',open_file),
    path('create_file/',create_file),
]