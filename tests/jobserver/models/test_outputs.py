import pytest
from django.conf import settings
from django.urls import reverse

from ...factories import (
    ReleaseFactory,
    ReviewFactory,
    ReviewRequestFactory,
    UserFactory,
    WorkspaceFactory,
)


@pytest.mark.django_db
def test_release_creation():
    release = ReleaseFactory(files=["file.txt"], upload_dir="workspace/release")

    assert str(release.file_path("file.txt")) == "releases/workspace/release/file.txt"


@pytest.mark.django_db
def test_release_get_absolute_url():
    release = ReleaseFactory()

    url = release.get_absolute_url()
    assert url == reverse(
        "workspace-release",
        kwargs={
            "org_slug": release.workspace.project.org.slug,
            "project_slug": release.workspace.project.slug,
            "workspace_slug": release.workspace.name,
            "release": release.id,
        },
    )


@pytest.mark.django_db
def test_release_file_path():
    files = {"file.txt": "test_release_creation"}
    release = ReleaseFactory(files=files)

    assert release.file_path("notextists") is None

    expected = (
        settings.RELEASE_STORAGE / f"{release.workspace.name}/{release.id}/file.txt"
    )
    path = release.file_path("file.txt")
    assert path == expected
    assert path.read_text() == "test_release_creation"

    path.unlink()
    assert release.file_path("file.txt") is None


@pytest.mark.django_db
def test_review_str():
    workspace = WorkspaceFactory(name="test-workspace")
    review_request = ReviewRequestFactory(workspace=workspace, created_by=UserFactory())
    review = ReviewFactory(review_request=review_request, status="accepted")

    assert str(review) == "accepted Review for test-workspace"


@pytest.mark.django_db
def test_reviewrequest_str():
    workspace = WorkspaceFactory(name="test-workspace")
    user = UserFactory(first_name="Ben")

    review_request = ReviewRequestFactory(workspace=workspace, created_by=user)

    expected = "Review requested by Ben for outputs from test-workspace"
    assert str(review_request) == expected
