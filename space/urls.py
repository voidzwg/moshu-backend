from django.urls import path
from .views import *

urlpatterns = [
    path('get_info/', get_info),
    path('update_info/', update_info),
    path('update_password/', update_password),
    path('get_group/', get_group)
]
