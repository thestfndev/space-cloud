from django.urls import path
from uploads import views

urlpatterns = [
    path("<int:pk>", views.UploadsTaskDetailView.as_view()),
    path("del/<int:pk>", views.DeleteUploadView.as_view()),
    path("new", views.CreateUploadView.as_view()),
    path("", views.ListUploadsView.as_view(), name="index"),
    path("header/<int:pk>", views.FitsHeaderUpdateView.as_view()),
]
