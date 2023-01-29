import pytest
from uploads.models import PENDING, UploadTask


@pytest.mark.django_db
def test_upload_task_defaults(client):
    task = UploadTask()
    task.save()
    assert task.filename == ""
    assert task.final_filename is None
    assert task.local_destination == ""
    assert task.timestamp is not None
    assert task.status == PENDING
    assert task.error_message is None
    assert task.initial_fits_header is None
    assert task.fits_header is None
