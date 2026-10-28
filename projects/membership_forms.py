from django import forms
from django.contrib.auth import get_user_model
from .models import ProjectMembership

User = get_user_model()


class ProjectMembershipForm(forms.ModelForm):
    class Meta:
        model = ProjectMembership
        fields = ["user", "can_reveal_secrets"]
        widgets = {
            "user": forms.Select(attrs={"class": "form-select"}),
            "can_reveal_secrets": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)

        if project:
            existing_ids = ProjectMembership.objects.filter(
                project=project
            ).values_list("user_id", flat=True)

            self.fields["user"].queryset = User.objects.exclude(
                pk=project.owner_id
            ).exclude(pk__in=existing_ids)