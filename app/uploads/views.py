import os
from pathlib import Path

from django.core.files.uploadedfile import UploadedFile
from django.http import JsonResponse
from fitsfiles.services import FitsService
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from uploads import serializers
from uploads.models import DONE, UploadTask

from app.settings import MEDIA_ROOT


class UploadsTaskDetailView(RetrieveUpdateAPIView):
    queryset = UploadTask.objects.all()
    serializer_class = serializers.DetailUploadTaskSerializer


class ListUploadsView(ListAPIView):

    queryset = UploadTask.objects.all()
    serializer_class = serializers.ListUploadTaskSerializer


def handle_uploaded_file(file: UploadedFile, destination: str):
    fname: str = file.name
    filepath = Path(MEDIA_ROOT, destination, fname)
    try:
        os.mkdir(Path(MEDIA_ROOT, destination))
    except FileExistsError:
        pass
    with filepath.open("wb") as uploaded_file:
        for chunk in file.chunks():
            uploaded_file.write(chunk)
        return (filepath, fname)


class CreateUploadView(CreateAPIView):
    serializer_class = serializers.UploadTaskInitializeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        destination = serializer.validated_data["destination"]

        filepath, filename = handle_uploaded_file(
            file=serializer.validated_data["file"], destination=destination
        )
        try:
            header = FitsService.get_file_header_dict(filepath)
        except OSError as exception:
            return Response(str(exception), status=status.HTTP_400_BAD_REQUEST)

        final_serializer = serializers.DetailUploadTaskSerializer(
            data={
                "filename": filename,
                "final_filename": filename,
                "status": DONE,
                "initial_fits_header": header,
                "local_destination": destination,
            }
        )
        final_serializer.is_valid(raise_exception=True)
        final_serializer.save()

        return JsonResponse(final_serializer.data)


class DeleteUploadView(DestroyAPIView):

    queryset = UploadTask.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        filepath = Path(MEDIA_ROOT, instance.local_destination, instance.final_filename)
        if os.path.isfile(filepath):
            filepath.unlink()
        instance.delete()
        return Response("ok")


class FitsHeaderUpdateView(UpdateAPIView):
    serializer_class = serializers.EditFitsHeaderSerializer
    queryset = UploadTask.objects.all()

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_object()
        # use already updated fits header if one exists, if not try using the
        # initial one, if both do not exist, initialize empty header
        current_header = instance.fits_header or instance.initial_fits_header or {}
        current_header.update(serializer.validated_data["header"])

        instance.fits_header = current_header

        instance.save()

        return Response("ok")
