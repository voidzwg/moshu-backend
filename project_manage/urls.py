from django.urls import path
from .views import *

urlpatterns = [
    path('get_project/', get_project),
    path('create/', create),
    path('rename/', rename),
    path('to_bin/', to_bin),
    path('out_bin/', out_bin),
    path('delete/', delete),
    path('close/', close),
    path('save_document/', save_document),
    path('get_document/', get_document),
    path('open_document/', open_document),
    path('create/',create),
    path('store/',store),
    path('get_documents/', get_documents),
    path('open_document/',open_document),
]
