from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from variables.models import EnvironmentVariable, VariableHistory
from .forms import EnvironmentVariableForm

from environments.models import Environment
from projects.models import ProjectMembership

from .services import create_variable, update_variable, delete_variable


from .services import delete_variable
from django.http import JsonResponse

@login_required
def variable_list(request, environment_id):

    environment = get_object_or_404(
        Environment,
        pk=environment_id,
    )

    project = environment.project

    is_owner = project.owner == request.user

    membership = ProjectMembership.objects.filter(
        project=project,
        user=request.user,
    ).first()

    if not is_owner and not membership:
        return HttpResponseForbidden("You don't have permission.")

    can_reveal_secrets = (
        is_owner or membership.can_reveal_secrets
    )

    variables = environment.variables.all()

    return render(
        request,
        "variables/variable_list.html",
        {
            "environment": environment,
            "variables": variables,
            "can_reveal_secrets": can_reveal_secrets,
        },
    )

@login_required
def variable_create(request, environment_id):

    environment = get_object_or_404(
        Environment,
        pk=environment_id,
    )

    project = environment.project

    is_owner = project.owner == request.user

    is_member = ProjectMembership.objects.filter(
        project=project,
        user=request.user,
    ).exists()

    if not is_owner and not is_member:
        return HttpResponseForbidden("You don't have permission.")

    if request.method == "POST":
        form = EnvironmentVariableForm(request.POST)

        if form.is_valid():
            create_variable(
                environment=environment,
                key=form.cleaned_data["key"],
                value=form.cleaned_data["value"],
                variable_type=form.cleaned_data["variable_type"],
                actor=request.user,
            )

            return redirect(
                "variable_list",
                environment_id=environment.id,
            )

    else:
        form = EnvironmentVariableForm()

    return render(
        request,
        "variables/variable_form.html",
        {
            "form": form,
            "environment": environment,
        },
    )

@login_required
def variable_edit(request, variable_id):

    variable = get_object_or_404(
    EnvironmentVariable,
        pk=variable_id,
    )

    project = variable.environment.project

    is_owner = project.owner == request.user

    is_member = ProjectMembership.objects.filter(
        project=project,
        user=request.user,
    ).exists()

    if not is_owner and not is_member:
        return HttpResponseForbidden("You don't have permission.")

    if request.method == "POST":
        form = EnvironmentVariableForm(request.POST)

        if form.is_valid():
            update_variable(
                variable_id=variable.id,
                new_key=form.cleaned_data["key"],
                new_value=form.cleaned_data["value"] or None,
                new_type=form.cleaned_data["variable_type"],
                actor=request.user,
            )

            return redirect(
                "variable_list",
                environment_id=variable.environment.id,
            )

    else:
     initial_value = ""

    if variable.variable_type == "standard":
        initial_value = variable.get_plaintext_value()

    form = EnvironmentVariableForm(initial={
        "key": variable.key,
        "value": initial_value,
        "variable_type": variable.variable_type,
    })

    return render(
        request,
        "variables/variable_form.html",
        {
            "form": form,
            "environment": variable.environment,
            "variable": variable,
        },
    )

@login_required
def variable_delete(request, variable_id):

    variable = get_object_or_404(
        EnvironmentVariable,
        pk=variable_id,
    )

    project = variable.environment.project

    is_owner = project.owner == request.user

    is_member = ProjectMembership.objects.filter(
        project=project,
        user=request.user,
    ).exists()

    if not is_owner and not is_member:
        return HttpResponseForbidden("You don't have permission.")

    if request.method == "POST":
        environment_id = variable.environment.id

        delete_variable(
            variable_id=variable.id,
            actor=request.user,
        )

        return redirect(
            "variable_list",
            environment_id=environment_id,
        )

    return render(
        request,
        "variables/variable_confirm_delete.html",
        {"variable": variable},
    )

@login_required
def variable_history(request, environment_id):

    environment = get_object_or_404(
        Environment,
        pk=environment_id,
    )

    project = environment.project

    is_owner = project.owner == request.user

    is_member = ProjectMembership.objects.filter(
        project=project,
        user=request.user,
    ).exists()

    if not is_owner and not is_member:
        return HttpResponseForbidden("You don't have permission.")

    history = VariableHistory.objects.filter(
    environment_name=str(environment)[:50]
).order_by("-created_at")
    return render(
        request,
        "variables/variable_history.html",
        {
            "environment": environment,
            "history": history,
        },
    )

@login_required
def reveal_variable(request, variable_id):

    variable = get_object_or_404(
        EnvironmentVariable,
        pk=variable_id,
    )

    project = variable.environment.project

    is_owner = project.owner == request.user

    membership = ProjectMembership.objects.filter(
        project=project,
        user=request.user,
    ).first()

    if not is_owner and not membership:
        return HttpResponseForbidden("You don't have permission.")

    can_reveal = is_owner or membership.can_reveal_secrets

    if not can_reveal:
        return HttpResponseForbidden("Secret reveal not permitted.")

    if variable.variable_type != "sensitive":
        return HttpResponseForbidden("This is not a sensitive variable.")

    response = JsonResponse({
        "value": variable.get_plaintext_value()
    })

    response["Cache-Control"] = "no-store"

    return response

@login_required
def variable_import(request, environment_id):
    environment = get_object_or_404(Environment, pk=environment_id)
    project = environment.project

    is_owner = project.owner == request.user
    is_member = ProjectMembership.objects.filter(
        project=project,
        user=request.user,
    ).exists()

    if not is_owner and not is_member:
        return HttpResponseForbidden("You don't have permission.")

    if request.method != "POST":
        return redirect("variable_list", environment_id=environment.id)

    env_text = request.POST.get("env_text", "")
    action = request.POST.get("action", "preview")

    entries = {}
    errors = []

    for line_number, line in enumerate(env_text.splitlines(), start=1):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            errors.append(f"Line {line_number}: Missing '='.")
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key or not key.replace("_", "a").isalnum():
            errors.append(f"Line {line_number}: Invalid variable name.")
            continue

        if key in entries:
            errors.append(f"Line {line_number}: Duplicate key '{key}'.")
            continue

        entries[key] = value

    if errors:
        return render(request, "variables/variable_import_preview.html", {
            "environment": environment,
            "errors": errors,
            "env_text": env_text,
        })

    existing = {
        variable.key: variable
        for variable in environment.variables.all()
    }

    preview = []

    for key, value in entries.items():
        old = existing.get(key)

        if old is None:
            status = "New"
            old_value = ""
            preview_value = value
        else:
            plain_old_value = old.get_plaintext_value()
            status = "Unchanged" if plain_old_value == value else "Update"

            old_value = (
                "••••••••"
                if old.variable_type == "sensitive"
                else plain_old_value
            )

            preview_value = (
                "••••••••"
                if old.variable_type == "sensitive"
                else value
            )

        preview.append({
            "key": key,
            "value": preview_value,
            "old_value": old_value,
            "status": status,
        })

    if action == "commit":
        with transaction.atomic():
            for item in preview:
                old = existing.get(item["key"])

                if old is None:
                    create_variable(
                        environment=environment,
                        key=item["key"],
                        value=item["value"],
                        variable_type="standard",
                        actor=request.user,
                    )
                elif item["status"] == "Update":
                    update_variable(
                        variable_id=old.id,
                        new_key=item["key"],
                        new_value=entries[item["key"]],
                        new_type=old.variable_type,
                        actor=request.user,
                    )

        return redirect("variable_list", environment_id=environment.id)

    return render(request, "variables/variable_import_preview.html", {
        "environment": environment,
        "preview": preview,
        "env_text": env_text,
    })