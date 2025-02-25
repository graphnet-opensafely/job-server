from django.utils import timezone
from first import first

from jobserver.models import Backend
from jobserver.views.status import Status

from ....factories import JobFactory, JobRequestFactory, StatsFactory
from ....utils import minutes_ago


def test_status_healthy(rf):
    tpp = Backend.objects.get(slug="tpp")

    # acked, because JobFactory will implicitly create JobRequests
    JobFactory.create_batch(3, job_request__backend=tpp)

    last_seen = minutes_ago(timezone.now(), 1)
    StatsFactory(backend=tpp, api_last_seen=last_seen)

    request = rf.get("/")
    response = Status.as_view()(request)

    tpp_output = first(
        response.context_data["backends"], key=lambda b: b["name"] == "TPP"
    )

    assert tpp_output["last_seen"] == last_seen.strftime("%Y-%m-%d %H:%M:%S")
    assert tpp_output["queue"]["acked"] == 3
    assert tpp_output["queue"]["unacked"] == 0
    assert not tpp_output["show_warning"]


def test_status_no_last_seen(rf):
    request = rf.get("/")
    response = Status.as_view()(request)

    tpp_output = first(
        response.context_data["backends"], key=lambda b: b["name"] == "TPP"
    )

    assert tpp_output["last_seen"] == "never"
    assert not tpp_output["show_warning"]


def test_status_unacked_jobs_but_recent_api_contact(rf):
    tpp = Backend.objects.get(slug="tpp")

    last_seen = minutes_ago(timezone.now(), 1)
    StatsFactory(backend=tpp, api_last_seen=last_seen)

    request = rf.get("/")
    response = Status.as_view()(request)

    tpp_output = first(
        response.context_data["backends"], key=lambda b: b["name"] == "TPP"
    )

    assert tpp_output["last_seen"] == last_seen.strftime("%Y-%m-%d %H:%M:%S")
    assert not tpp_output["show_warning"]


def test_status_unhealthy(rf):
    # backends are created by migrations so we can depend on them
    tpp = Backend.objects.get(slug="tpp")

    # acked, because JobFactory will implicitly create JobRequests
    JobFactory.create_batch(2, job_request__backend=tpp)

    # unacked, because it has no Jobs
    JobRequestFactory(backend=tpp)

    last_seen = minutes_ago(timezone.now(), 10)
    StatsFactory(backend=tpp, api_last_seen=last_seen, url="foo")

    request = rf.get("/")
    response = Status.as_view()(request)

    tpp_output = first(
        response.context_data["backends"], key=lambda b: b["name"] == "TPP"
    )

    assert tpp_output["last_seen"] == last_seen.strftime("%Y-%m-%d %H:%M:%S")
    assert tpp_output["queue"]["acked"] == 2
    assert tpp_output["queue"]["unacked"] == 1
    assert tpp_output["show_warning"]
