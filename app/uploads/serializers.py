from rest_framework import serializers
from uploads.models import UploadTask


class DetailUploadTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadTask
        fields = "__all__"


class ListUploadTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadTask
        fields = ["filename", "timestamp", "status"]


class UploadTaskInitializeSerializer(serializers.Serializer):
    destination = serializers.CharField()
    file = serializers.FileField()


class EditFitsHeaderSerializer(serializers.Serializer):

    header = serializers.DictField()
