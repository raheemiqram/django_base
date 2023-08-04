from django.core.exceptions import ValidationError
from django.db.models import Q
from django.template import Context
from django.template.backends.django import Template

from apps.users.models import User


def get_filter(filter_name, filter_operator, filter_value):
    """
    This function should generate queryset filter format with values
    """

    customer = User.objects.all()
    if filter_operator == "range":
        filter_value = list(filter_value.split(","))

    if filter_name == "all_customer":
        # possible value = yes or no
        kwargs = {}
        if filter_value == "yes":
            kwargs = {"id__in": list(customer.values_list("id", flat=True))}
        return Q(**kwargs)

    if filter_name == "is_super_user":
        if filter_value.lower() in ["yes", "true"]:
            kwargs = {"is_superuser": True}
        else:
            kwargs = {"is_superuser": False}
        return Q(**kwargs)

    if filter_name == "is_staff":
        if filter_value.lower() in ["yes", "true"]:
            kwargs = {"is_staff": True}
        else:
            kwargs = {"is_staff": False}
        return Q(**kwargs)

    if filter_name == "custom_customer":
        # possible value comma separate user ids
        kwargs = {"id__in": list(map(int, filter_value.split(",")))}
        return Q(**kwargs)

    if filter_name == "name":
        # possible value strings
        first_condition = get_operators(filter_operator, filter_name, "first_name")
        last_condition = get_operators(filter_operator, filter_name, "last_name")
        kwargs1 = {first_condition: filter_value}
        kwargs2 = {last_condition: filter_value}
        first_condition = Q(**kwargs1)
        last_condition = Q(**kwargs2)
        return first_condition | last_condition

    if filter_name == "email":
        # possible value strings
        condition = get_operators(filter_operator, filter_name, "email")
        kwargs = {condition: filter_value}
        return Q(**kwargs)


def get_operators(filter_operator, filter_name, field_name):
    if filter_operator.strip() == "icontains":
        return f"{field_name}__icontains"

    if filter_operator.strip() == "not_equal":
        return f"{field_name}__iexact"

    if filter_operator.strip() == "starts_with":
        return f"{field_name}__istartswith"

    if filter_operator.strip() == "equal":
        return f"{field_name}__iexact"

    if filter_operator.strip() == "not_equal":
        return f"{field_name}__iexact"

    if filter_operator.strip() == "gt":
        return f"{field_name}__gt"

    if filter_operator.strip() == "gte":
        return f"{field_name}__gte"

    if filter_operator.strip() == "lt":
        return f"{field_name}__lt"

    if filter_operator.strip() == "lte":
        return f"{field_name}__lte"

    if filter_operator.strip() == "range":
        return f"{field_name}__range"
    raise ValidationError(f'Resolved field "{filter_name}" with "{filter_operator}" lookup is not a valid type')


def render_notification_template(template, data):
    template = Template(template)
    return template.render(Context(data))  # dict(user=user, order=order)))