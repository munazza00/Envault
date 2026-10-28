from django.db import models
from environments.models import Environment
from .encryption import encrypt_value, decrypt_value
from django.conf import settings


class EnvironmentVariable(models.Model):

    VARIABLE_TYPES = [
        ("standard", "Standard"),
        ("sensitive", "Sensitive"),
    ]

    environment = models.ForeignKey(
        Environment,
        on_delete=models.CASCADE,
        related_name="variables",
    )

    key = models.CharField(max_length=255)

    value = models.TextField()

    variable_type = models.CharField(
        max_length=20,
        choices=VARIABLE_TYPES,
        default="standard",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
    _plaintext_value = None

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["environment", "key"],
                name="unique_variable_per_environment",
            )
        ]

    def set_plaintext_value(self, plaintext):
        self._plaintext_value = plaintext

    def get_plaintext_value(self):
        if self.variable_type == "sensitive":
            return decrypt_value(self.value)

        return self.value

    def save(self, *args, **kwargs):
        existing = None

        if self.pk:
            existing = type(self).objects.filter(
                pk=self.pk
            ).values("value", "variable_type").first()

        if self._plaintext_value is not None:
            plaintext = self._plaintext_value
        elif existing:
            old_value = existing["value"]
            old_type = existing["variable_type"]

            if old_type != self.variable_type:
                if old_type == "sensitive":
                    plaintext = decrypt_value(old_value)
                else:
                    plaintext = old_value
            else:
                self.value = old_value
                plaintext = None
        else:
            plaintext = self.value

        if plaintext is not None:
            if self.variable_type == "sensitive":
                self.value = encrypt_value(plaintext)
            else:
                self.value = plaintext

        self._plaintext_value = None
        super().save(*args, **kwargs)
class VariableHistory(models.Model):

    ACTION_TYPES = [
        ("created", "Created"),
        ("updated", "Updated"),
        ("classification_changed", "Classification Changed"),
        ("deleted", "Deleted"),
    ]

    variable = models.ForeignKey(
        EnvironmentVariable,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="history",
    )

    variable_key = models.CharField(max_length=255)

    environment_name = models.CharField(max_length=50)

    action = models.CharField(
        max_length=30,
        choices=ACTION_TYPES,
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="variable_history",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.variable_key} - {self.get_action_display()}"