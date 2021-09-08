import pytest


@pytest.mark.django_db
def test_get_application(client):
    rsp = client.get("/applications/")
    assert rsp.status_code == 200
