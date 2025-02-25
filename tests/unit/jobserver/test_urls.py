import inspect

import pytest
from django.contrib.auth.views import LogoutView
from django.urls import resolve
from social_django.views import auth as social_django_auth_view

from jobserver.api.jobs import (
    JobAPIUpdate,
    JobRequestAPIList,
    UserAPIDetail,
    WorkspaceStatusesAPI,
)
from jobserver.api.releases import (
    ReleaseAPI,
    ReleaseFileAPI,
    ReleaseNotificationAPICreate,
    ReleaseWorkspaceAPI,
    SnapshotAPI,
    SnapshotCreateAPI,
    SnapshotPublishAPI,
    WorkspaceStatusAPI,
)
from jobserver.utils import dotted_path
from jobserver.views import (
    admin,
    index,
    job_requests,
    jobs,
    orgs,
    projects,
    releases,
    status,
    users,
    workspaces,
)
from staff.views import backends as staff_backends
from staff.views import projects as staff_projects
from staff.views import users as staff_users
from staff.views import workspaces as staff_workspaces


@pytest.mark.parametrize(
    "url,redirect",
    [
        ("/favicon.ico", "/static/favicon.ico"),
        ("/event-list/", "/event-log/"),
        ("/jobs/", "/event-log/"),
        ("/workspaces/", "/"),
    ],
)
def test_url_redirects(client, url, redirect):
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == redirect


@pytest.mark.parametrize(
    "url,view",
    [
        ("/", index.Index),
        ("/admin/approve-users", admin.ApproveUsers),
        ("/api/v2/job-requests/", JobRequestAPIList),
        ("/api/v2/jobs/", JobAPIUpdate),
        ("/api/v2/release-notifications/", ReleaseNotificationAPICreate),
        ("/api/v2/users/ben/", UserAPIDetail),
        ("/api/v2/workspaces/w/statuses/", WorkspaceStatusesAPI),
        ("/api/v2/workspaces/w/snapshots", SnapshotCreateAPI),
        ("/api/v2/workspaces/w/snapshots/42", SnapshotAPI),
        ("/api/v2/workspaces/w/snapshots/42/publish", SnapshotPublishAPI),
        ("/api/v2/workspaces/w/status", WorkspaceStatusAPI),
        ("/api/v2/releases/workspace/w", ReleaseWorkspaceAPI),
        ("/api/v2/releases/release/42", ReleaseAPI),
        ("/api/v2/releases/file/42", ReleaseFileAPI),
        ("/event-log/", job_requests.JobRequestList),
        ("/staff/backends/", staff_backends.BackendList),
        ("/staff/backends/42/", staff_backends.BackendDetail),
        ("/staff/backends/42/edit/", staff_backends.BackendEdit),
        ("/staff/backends/42/rotate-token/", staff_backends.BackendRotateToken),
        ("/staff/projects/", staff_projects.ProjectList),
        ("/staff/projects/p/", staff_projects.ProjectDetail),
        ("/staff/projects/p/edit/", staff_projects.ProjectEdit),
        ("/staff/users/", staff_users.UserList),
        ("/staff/users/<username>/", staff_users.UserDetail),
        ("/staff/workspaces/", staff_workspaces.WorkspaceList),
        ("/staff/workspaces/w/", staff_workspaces.WorkspaceDetail),
        ("/job-requests/42/", job_requests.JobRequestDetailRedirect),
        ("/jobs/<identifier>/", jobs.JobDetailRedirect),
        ("/login/github/", social_django_auth_view),
        ("/logout/", LogoutView),
        ("/orgs/", orgs.OrgList),
        ("/orgs/new/", orgs.OrgCreate),
        ("/settings/", users.Settings),
        ("/status/", status.Status),
        ("/o/", orgs.OrgDetail),
        ("/o/new-project/", projects.ProjectCreate),
        ("/o/project-onboarding/", projects.ProjectOnboardingCreate),
        ("/o/p/", projects.ProjectDetail),
        ("/o/p/accept-invite/42/", projects.ProjectAcceptInvite),
        ("/o/p/cancel-invite/", projects.ProjectCancelInvite),
        ("/o/p/invite-users/", projects.ProjectInvitationCreate),
        ("/o/p/members/42/edit", projects.ProjectMembershipEdit),
        ("/o/p/members/42/remove", projects.ProjectMembershipRemove),
        ("/o/p/new-workspace/", workspaces.WorkspaceCreate),
        ("/o/p/releases/", releases.ProjectReleaseList),
        ("/o/p/settings/", projects.ProjectSettings),
        ("/o/p/w/", workspaces.WorkspaceDetail),
        ("/o/p/w/run-jobs/", job_requests.JobRequestCreate),
        ("/o/p/w/archive-toggle/", workspaces.WorkspaceArchiveToggle),
        ("/o/p/w/files/", workspaces.WorkspaceFileList),
        ("/o/p/w/files/tpp/", workspaces.WorkspaceBackendFiles),
        ("/o/p/w/files/tpp/file.txt", workspaces.WorkspaceBackendFiles),
        ("/o/p/w/logs/", workspaces.WorkspaceLog),
        ("/o/p/w/notifications-toggle/", workspaces.WorkspaceNotificationsToggle),
        ("/o/p/w/outputs/", workspaces.WorkspaceOutputList),
        ("/o/p/w/outputs/latest/", workspaces.WorkspaceLatestOutputsDetail),
        ("/o/p/w/outputs/latest/download/", workspaces.WorkspaceLatestOutputsDownload),
        ("/o/p/w/outputs/latest/file.txt", workspaces.WorkspaceLatestOutputsDetail),
        ("/o/p/w/outputs/badge/", workspaces.WorkspaceOutputsBadge),
        ("/o/p/w/outputs/42/", releases.SnapshotDetail),
        ("/o/p/w/outputs/42/download/", releases.SnapshotDownload),
        ("/o/p/w/outputs/42/file.txt", releases.SnapshotDetail),
        ("/o/p/w/releases/", releases.WorkspaceReleaseList),
        ("/o/p/w/releases/42/", releases.ReleaseDetail),
        ("/o/p/w/releases/42/download/", releases.ReleaseDownload),
        ("/o/p/w/releases/42/abc/delete/", releases.ReleaseFileDelete),
        ("/o/p/w/releases/42/file.txt", releases.ReleaseDetail),
        ("/o/p/w/42/", job_requests.JobRequestDetail),
        ("/o/p/w/42/cancel/", job_requests.JobRequestCancel),
        ("/o/p/w/42/abc/", jobs.JobDetail),
        ("/o/p/w/42/abc/cancel/", jobs.JobCancel),
    ],
)
def test_url_resolution(url, view):
    """Test each URL resolves to the expected view function or class"""
    resolved_view = resolve(url).func

    assert dotted_path(resolved_view) == dotted_path(view), url

    msg = f"Resolved view '{resolved_view}' is a class. Did you forget `.as_view()`?"
    assert not inspect.isclass(resolved_view), msg
