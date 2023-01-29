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
def test_not_uploads_list(client):
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
