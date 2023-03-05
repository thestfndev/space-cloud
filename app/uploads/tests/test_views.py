from io import BytesIO
from unittest.mock import patch

import pytest
from django.urls import reverse
from uploads.models import UploadTask


@pytest.mark.django_db
def test_empty_uploads_list(client):
    url = reverse("index")
    response = client.get(url)
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_uploads_list(client):
    for _ in range(3):
        UploadTask.objects.create(
            filename="pic.fits", local_destination="test", status="Done"
        )
    url = reverse("index")
    response = client.get(url)
    assert response.status_code == 200
    assert response.data != []
    assert len(response.data) == 3
    for upload in response.data:
        assert upload["filename"] == "pic.fits"
        assert upload["timestamp"] is not None
        assert upload["status"] == "Done"


@pytest.mark.django_db
@patch("fitsfiles.services.FitsService.get_file_header_dict", return_value={})
def test_upload_creation(_, client):
    test_image = BytesIO(b"mybinarydata")
    test_image.name = "myimage.fits"
    url = reverse("upload-new")

    response = client.post(url, {"file": test_image, "destination": "dest"})

    uploaded_pk = response.content.decode()
    assert response.status_code == 200
    upload = UploadTask.objects.get(pk=uploaded_pk)
    assert upload.id == int(uploaded_pk)
    assert upload.filename == "myimage.fits"
    assert upload.final_filename == "myimage.fits"
    assert upload.local_destination == "dest"
    assert upload.status == "Done"
    assert upload.error_message is None
    assert upload.initial_fits_header == {}
    assert upload.fits_header is None


@pytest.mark.django_db
def test_upload_deletion(client):
    instance = UploadTask.objects.create(
        filename="pic.fits",
        final_filename="pic.fits",
        local_destination="test",
        status="Done",
    )
    url = reverse("upload-delete", kwargs={"pk": instance.pk})
    response = client.delete(url)
    assert response.status_code == 200
    assert UploadTask.objects.filter(pk=instance.pk).count() == 0
