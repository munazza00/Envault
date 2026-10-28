from django.contrib import admin
from .models import EnvironmentVariable, VariableHistory


admin.site.register(EnvironmentVariable)
admin.site.register(VariableHistory)