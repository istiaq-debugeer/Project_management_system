from django.db import models
from django.conf import settings
from core.base_model import TimeStampedModel
from projects.models import Project


class Task(TimeStampedModel):
    STATUS_CHOICES = [
        ("ToDo", "To Do"),
        ("InProgress", "In Progress"),
        ("Done", "Done"),
    ]

    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ToDo")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="LOW")

    # One task belongs to one project
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="tasks", db_index=True
    )

    # A task can be assigned to one or more users
    assigned_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="tasks", blank=True, db_index=True
    )

    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class comments(TimeStampedModel):
    content = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="comments",
        on_delete=models.CASCADE,
        db_index=True,
    )
    tasks = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="task_comments", db_index=True
    )
