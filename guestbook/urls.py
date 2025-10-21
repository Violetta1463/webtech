from django.urls import path
from .views import guestbook_view, guestbook_detail, guestbook_edit, guestbook_delete, signup
from .views import (
    EntryListView, EntryDetailView, EntryCreateView, EntryUpdateView, EntryDeleteView
)

urlpatterns = [
    path('', EntryListView.as_view(), name='guestbook'),
    path('<int:pk>/', EntryDetailView.as_view(), name='guestbook-detail'),
    path('create/', EntryCreateView.as_view(), name='guestbook-create'),
    path('<int:pk>/edit/', EntryUpdateView.as_view(), name='guestbook-edit'),
    path('<int:pk>/delete/', EntryDeleteView.as_view(), name='guestbook-delete'),
]
