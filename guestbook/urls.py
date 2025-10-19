from django.urls import path
from .views import guestbook_view, guestbook_detail, guestbook_edit, guestbook_delete

urlpatterns = [
    path('', guestbook_view, name='guestbook'),
    path('<int:pk>/', guestbook_detail, name='guestbook-detail'),
    path('<int:pk>/edit/', guestbook_edit, name='guestbook-edit'),
    path('<int:pk>/delete/', guestbook_delete, name='guestbook-delete'),
]
