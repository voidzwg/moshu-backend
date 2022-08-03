from django.urls import path
from .views import *

urlpatterns = [
    path('get_member/', get_member),
    path('appoint/',appoint),
    path('delete/',delete),
    path('revoke/',revoke)
]
