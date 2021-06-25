import json

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Release(models.Model):
    """Reviewed and redacted outputs from a Workspace"""

    # No value in the default Autoid as we are using a content-addressable hash
    # as it. Additionaly it avoids enumeration attacks.
    id = models.TextField(primary_key=True)
    # TODO: link this formally via backend_username once we have a mapping
    # between User and their backend username
    publishing_user = models.ForeignKey(
        "User",
        on_delete=models.PROTECT,
        null=True,
        related_name="+",
    )
    workspace = models.ForeignKey(
        "Workspace",
        on_delete=models.PROTECT,
        related_name="releases",
    )
    backend = models.ForeignKey(
        "Backend",
        on_delete=models.PROTECT,
        related_name="+",
    )
    published_at = models.DateTimeField(default=timezone.now)
    upload_dir = models.TextField()
    # list of files in the release upload
    files = models.JSONField()
    # store local TPP/EMIS username for audit
    backend_user = models.TextField()

    def get_absolute_url(self):
        return reverse(
            "workspace-release",
            kwargs={
                "org_slug": self.workspace.project.org.slug,
                "project_slug": self.workspace.project.slug,
                "workspace_slug": self.workspace.name,
                "release": self.id,
            },
        )

    def file_path(self, filepath):
        if filepath not in self.files:
            return None
        abs_path = settings.RELEASE_STORAGE / self.upload_dir / filepath
        if not abs_path.exists():
            return None
        return abs_path

    @property
    def manifest(self):
        return json.loads(self.file_path("metadata/manifest.json").read_text())


class Review(models.Model):
    STATUS_CHOICES = [
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    reviewer = models.ForeignKey(
        "User",
        on_delete=models.PROTECT,
        related_name="reviews",
    )
    review_request = models.ForeignKey(
        "ReviewRequest",
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    status = models.TextField(choices=STATUS_CHOICES)
    message = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.status} Review for {self.review_request.workspace.name}"


class ReviewRequest(models.Model):
    """Models a request from a Researcher to review some outputs in a Workspace."""

    backend = models.ForeignKey(
        "Backend",
        on_delete=models.PROTECT,
        related_name="review_requests",
    )
    created_by = models.ForeignKey(
        "User",
        on_delete=models.PROTECT,
        related_name="review_requests",
    )
    previous_request = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="previous_requests",
        null=True,
    )
    release = models.ForeignKey(
        "Release",
        on_delete=models.CASCADE,
        related_name="review_requests",
    )
    workspace = models.ForeignKey(
        "Workspace",
        on_delete=models.CASCADE,
        related_name="review_requests",
    )

    # file paths from the backend
    paths = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review requested by {self.created_by.name} for outputs from {self.workspace.name}"
