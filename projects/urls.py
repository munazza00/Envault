from django.urls import path
from . import views

urlpatterns = [
    path("", views.project_dashboard, name="project_dashboard"),
    path("create/", views.create_project, name="create_project"),
    path(
    "<int:project_id>/members/",
    views.manage_members,
    name="manage_members",
),
path(
    "<int:project_id>/",
    views.project_detail,
    name="project_detail",
),
]