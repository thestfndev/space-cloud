import logging
import os

import boto3
from botocore.exceptions import ClientError
from uploads.repository import UploadTaskRepository


class UploadTaskService:
    def __init__(self):
        self.repo = UploadTaskRepository()

    # TODO: move this to separate service
    def upload_file_to_s3(self, id: int):
        AWS_BUCKET = os.getenv("AWS_BUCKET")

        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        full = self.repo.get_full_local_path(id=id)
        relative = self.repo.get_local_path(id=id)

        s3_client = boto3.client("s3")
        try:
            s3_client.upload_file(full, AWS_BUCKET, str(relative))
        except ClientError as e:
            logging.error(e)
            return False
        return True
