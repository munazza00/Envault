from django.db import models
from projects.models import Project


class Environment(models.Model):
    ENVIRONMENT_CHOICES = [
        ("development", "Development"),
        ("staging", "Staging"),
        ("production", "Production"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="environments",
    )
    name = models.CharField(
        max_length=30,
        choices=ENVIRONMENT_CHOICES,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "name"],
                name="unique_environment_per_project",
            )
        ]

    def __str__(self):
        return f"{self.project.name} - {self.get_name_display()}"