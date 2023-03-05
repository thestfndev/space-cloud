from pathlib import Path

from uploads.models import UploadTask

from app.settings import MEDIA_ROOT


class UploadTaskRepository:
    def get(self, id: int) -> UploadTask:
        return UploadTask.objects.get(pk=id)

    def get_full_local_path(self, id: int) -> Path:
        upload = self.get(id=id)
        return Path(MEDIA_ROOT, upload.local_destination, upload.final_filename)

    def get_local_path(self, id: int) -> Path:
        upload = self.get(id=id)
        return Path(upload.local_destination, upload.final_filename)

    def get_file(self, id: int) -> Path:
        path = self.get_full_local_path(id=id)
        with open(path, "rb") as fff:
            return fff
