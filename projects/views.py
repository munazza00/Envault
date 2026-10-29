from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponseForbidden

from .models import Project, ProjectMembership
from .forms import ProjectForm
from .membership_forms import ProjectMembershipForm
from environments.models import Environment


@login_required
def project_dashboard(request):
    projects = Project.objects.filter(
        Q(owner=request.user) |
        Q(memberships__user=request.user)
    ).distinct()

    return render(
        request,
        "projects/dashboard.html",
        {"projects": projects},
    )

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.filter(
            Q(owner=request.user) |
            Q(memberships__user=request.user)
        ).distinct(),
        pk=project_id,
    )

    environments = project.environments.all()
    members = project.memberships.select_related("user").all()

    return render(
        request,
        "projects/detail.html",
        {
            "project": project,
            "environments": environments,
            "members": members,
        },
    )


@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect("project_dashboard")
    else:
        form = ProjectForm()

    return render(
        request,
        "projects/create_project.html",
        {"form": form},
    )


@login_required
def manage_members(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if project.owner != request.user:
        return HttpResponseForbidden("Only the project owner can manage members.")

    if request.method == "POST":
        form = ProjectMembershipForm(request.POST)

        if form.is_valid():
            membership = form.save(commit=False)
            membership.project = project
            membership.save()
            return redirect("project_dashboard")
    else:
        form = ProjectMembershipForm(project=project)

    return render(
        request,
        "projects/manage_members.html",
        {
            "project": project,
            "form": form,
        },
    )