from django.urls import path
from .views import *

urlpatterns = [
    path('store/', store),
    path('get_design/', get_design)
]
