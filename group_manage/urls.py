from django.urls import path
from .views import *

urlpatterns = [
    path('create_group/', create_group),
    path('get_created_group/', get_created_group),
    path('get_managed_group/', get_managed_group),
    path('get_participated_group/', get_participated_group)
]
