from django.urls import path
from .views import *

urlpatterns = [
    path('get_member/', get_member),
    path('appoint/',appoint),
    path('delete/',delete),
    path('revoke/',revoke),
    path('get_user/',get_user),
    path('invite/',invite),
    path('accept_invition/',accept_invition),
]
