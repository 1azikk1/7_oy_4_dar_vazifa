
from django.contrib.auth.decorators import user_passes_test


def user_staff_required(function=None, redirect_field_name=None, login_url='404'):
    actual_decorator = user_passes_test(
        lambda user: user.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

