from celery import shared_task
from uploads.service import UploadTaskService


@shared_task
def export_to_s3(id):
    uts = UploadTaskService()
    uts.upload_file_to_s3(id)
