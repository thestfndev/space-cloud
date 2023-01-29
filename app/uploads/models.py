from django.db import models

PENDING = "Pending"
INPROGRESS = "In Progress"
DONE = "Done"
ERROR = "Error"

TASK_STATUS = [
    (PENDING, "Pending"),
    (INPROGRESS, "In Progress"),
    (DONE, "Done"),
    (ERROR, "Error"),
]


class UploadTask(models.Model):
    filename = models.CharField(max_length=256)
    final_filename = models.CharField(max_length=256, null=True)
    local_destination = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=TASK_STATUS, default=PENDING)
    error_message = models.CharField(max_length=256, null=True)
    initial_fits_header = models.JSONField(null=True)
    fits_header = models.JSONField(null=True)
