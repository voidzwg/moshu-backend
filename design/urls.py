from django.urls import path
from .views import *

urlpatterns = [
    path('store/', store),
    path('create/', create),
    path('rename/', rename),
    path('delete/', delete),
    path('get_design/', get_design),
    path('get_one_design/', get_one_design),
    path('search_design/', search_design),
    path('get_templates/',get_templates),
    path('open_template/',open_template),
]
