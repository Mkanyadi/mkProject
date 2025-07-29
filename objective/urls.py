from .views import ObjectiveMemoryUpdateView
from . import views
from django.urls import path
from .views import (
    home,
    BucketListView,
    ObjectiveListView,
    ObjectiveDetailView,
    ObjectiveCreateView,
    ObjectiveUpdateView,
    ObjectiveDeleteView,
    AddObjectiveFromBucketView,
    toggle_completed
)

urlpatterns = [
    path('', home, name='home'),
    path('list/', ObjectiveListView.as_view(), name='objective-list'),
    path('add/', ObjectiveCreateView.as_view(), name='objective-add'),
    path('<int:pk>/', ObjectiveDetailView.as_view(), name='objective-detail'),
    path('<int:pk>/edit/', ObjectiveUpdateView.as_view(), name='objective-edit'),
    path('<int:pk>/delete/', ObjectiveDeleteView.as_view(), name='objective-delete'),
    path('bucket-list/', BucketListView.as_view(), name='bucket-list'),
    path('bucket-list/add/', AddObjectiveFromBucketView.as_view(), name='add-from-bucket'),
    path('toggle-completed/<int:pk>/', toggle_completed, name='toggle-completed'),
    path('objectives/bucket-list/', BucketListView.as_view(), name='bucket-list'),
    path('<int:pk>/memory/', ObjectiveMemoryUpdateView.as_view(), name='objective-memory-update'),
]
