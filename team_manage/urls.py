from django.urls import path
from .views import *

urlpatterns = [
    path('get_member/', get_member),
    path('appoint/',appoint),
    path('delete/',delete),
    path('revoke/',revoke),
    path('get_user/',get_user),
    path('invite/',invite),
    path('get_invitation/', get_invitation),
    path('accept_invitation/',accept_invitation),
    path('read_invitation/', read_invitation),
    path('delete_invitation/', delete_invitation),
]
