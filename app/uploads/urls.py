from django.urls import path
from uploads import views

urlpatterns = [
    path("<int:pk>", views.UploadsTaskDetailView.as_view(), name="upload-detail"),
    path("del/<int:pk>", views.DeleteUploadView.as_view(), name="upload-delete"),
    path("new", views.CreateUploadView.as_view(), name="upload-new"),
    path("", views.ListUploadsView.as_view(), name="index"),
    path(
        "header/<int:pk>",
        views.FitsHeaderUpdateView.as_view(),
        name="upload-header-update",
    ),
]
