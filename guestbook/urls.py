from django.urls import path
from .views import guestbook_view

urlpatterns = [
    path('', guestbook_view, name='guestbook'),
]
