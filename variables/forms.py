from django import forms
from .models import EnvironmentVariable


class EnvironmentVariableForm(forms.ModelForm):

    class Meta:
        model = EnvironmentVariable
        fields = ["key", "variable_type"]

    value = forms.CharField(
    required=False,
    widget=forms.Textarea(attrs={
        "rows": 3,
        "placeholder": "Leave blank to keep the existing value",
    })
)