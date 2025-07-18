from django.urls import path
from .views import (
    home,
    ObjectiveListView,
    ObjectiveDetailView,
    ObjectiveCreateView,
    ObjectiveUpdateView,
    ObjectiveDeleteView,
)

urlpatterns = [
    path('', home, name='home'),
    path('list/', ObjectiveListView.as_view(), name='objective-list'),
    path('add/', ObjectiveCreateView.as_view(), name='objective-add'),
    path('<int:pk>/', ObjectiveDetailView.as_view(), name='objective-detail'),
    path('<int:pk>/edit/', ObjectiveUpdateView.as_view(), name='objective-edit'),
    path('<int:pk>/delete/', ObjectiveDeleteView.as_view(), name='objective-delete'),
]
