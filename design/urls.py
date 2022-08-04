from django.urls import path
from .views import *

urlpatterns = [
    path('store/', store),
    path('create/', create),
    path('rename/', rename),
    path('delete/', delete),
    path('get_design/', get_design)
]
