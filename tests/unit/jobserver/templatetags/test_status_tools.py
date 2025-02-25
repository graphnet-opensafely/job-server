from jobserver.models import Backend
from jobserver.templatetags.status_tools import status_hint

from ....factories import (
    BackendFactory,
    JobFactory,
    JobRequestFactory,
    WorkspaceFactory,
)


# "dependency_failed"
# "waiting_on_dependencies"
# "waiting_on_workers"


def test_status_hint_dependency_failed():
    backend = Backend.objects.get(slug="tpp")
    job_request = JobRequestFactory(backend=backend)
    job = JobFactory(job_request=job_request, status_code="dependency_failed")

    assert status_hint(job) == ""


def test_status_hint_waiting_on_dependencies():
    backend = Backend.objects.get(slug="tpp")
    job_request = JobRequestFactory(backend=backend)
    job = JobFactory(job_request=job_request, status_code="waiting_on_dependencies")

    assert status_hint(job) == ""


def test_status_hint_waiting_on_workers():
    backend = Backend.objects.get(slug="tpp")
    job_request = JobRequestFactory(backend=backend)
    job = JobFactory(job_request=job_request, status_code="waiting_on_workers")

    assert status_hint(job) == ""


def test_status_hint_nonzero_exit():
    backend = Backend.objects.get(slug="tpp")
    workspace = WorkspaceFactory(name="an-workspace")
    job_request = JobRequestFactory(backend=backend, workspace=workspace)
    job = JobFactory(
        job_request=job_request,
        action="test_action",
        status_code="nonzero_exit",
    )

    output = status_hint(job)

    path = f"{backend.parent_directory}/an-workspace/metadata/test_action.log"
    assert path in output


def test_status_hint_unknown_backend():
    backend = BackendFactory()
    job_request = JobRequestFactory(backend=backend)
    job = JobFactory(job_request=job_request)

    assert status_hint(job) == ""


def test_status_hint_unknown_status_code():
    backend = Backend.objects.get(slug="tpp")
    job_request = JobRequestFactory(backend=backend)
    job = JobFactory(job_request=job_request)

    assert status_hint(job) == ""
