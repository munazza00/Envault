from django.db import transaction
from .models import EnvironmentVariable, VariableHistory


def record_variable_history(variable, action, actor):
    VariableHistory.objects.create(
        variable=variable,
        variable_key=variable.key,
        environment_name=str(variable.environment)[:50],
        action=action,
        actor=actor,
    )

@transaction.atomic
def create_variable(environment, key, value, variable_type, actor):
    variable = EnvironmentVariable(
        environment=environment,
        key=key,
        variable_type=variable_type,
    )

    variable.set_plaintext_value(value)
    variable.save()

    record_variable_history(variable, "created", actor)

    return variable

@transaction.atomic
def update_variable(variable_id, new_key, new_value, new_type, actor):
    variable = EnvironmentVariable.objects.select_for_update().get(
        pk=variable_id
    )

    old_value = variable.get_plaintext_value()
    old_type = variable.variable_type

    key_changed = variable.key != new_key
    value_changed = (
    new_value is not None and old_value != new_value
)
    type_changed = old_type != new_type

    if not key_changed and not value_changed and not type_changed:
        return variable

    variable.key = new_key
    variable.variable_type = new_type

    if value_changed:
        variable.set_plaintext_value(new_value)

    variable.save()

    if key_changed or value_changed:
        record_variable_history(
            variable=variable,
            action="updated",
            actor=actor,
        )

    if type_changed:
        record_variable_history(
            variable=variable,
            action="classification_changed",
            actor=actor,
        )

    return variable

@transaction.atomic
def delete_variable(variable_id, actor):
    variable = EnvironmentVariable.objects.select_for_update().get(
        pk=variable_id
    )

    record_variable_history(variable, "deleted", actor)
    variable.delete()