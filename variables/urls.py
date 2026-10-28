from django.urls import path
from . import views

urlpatterns = [
    path(
        "environment/<int:environment_id>/",
        views.variable_list,
        name="variable_list",
    ),
    path(
        "environment/<int:environment_id>/create/",
        views.variable_create,
        name="variable_create",
    ),
    path(
        "<int:variable_id>/edit/",
        views.variable_edit,
        name="variable_edit",
    ),
    path(
        "<int:variable_id>/delete/",
        views.variable_delete,
        name="variable_delete",
    ),
    path(
    "environment/<int:environment_id>/history/",
    views.variable_history,
    name="variable_history",
),
path(
    "<int:variable_id>/reveal/",
    views.reveal_variable,
    name="reveal_variable",
),
path(
    "environment/<int:environment_id>/import/",
    views.variable_import,
    name="variable_import",
),

]