from django.urls import path
from .views import (
    BadgeListView,
    BadgeDetailView,
    BadgeCreateView,
    BadgeUpdateView,
    BadgeDeleteView
)

urlpatterns = [
    path('', BadgeListView.as_view(), name='badge-list'),
    path('<int:pk>/', BadgeDetailView.as_view(), name='badge-detail'),
    path('create/', BadgeCreateView.as_view(), name='badge-create'),
    path('<int:pk>/update/', BadgeUpdateView.as_view(), name='badge-update'),
    path('<int:pk>/delete/', BadgeDeleteView.as_view(), name='badge-delete'),
]
