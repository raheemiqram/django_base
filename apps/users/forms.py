from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core import exceptions, validators
from django.utils.translation import gettext_lazy as _, pgettext

from allauth.account import app_settings
from allauth.account.utils import perform_login
from allauth.account.adapter import get_adapter
from allauth.account.forms import PasswordField, SetPasswordField
from allauth.utils import set_form_field_order, get_username_max_length

from apps.core.enums import AuthenticationMethod
from apps.users.models import User


class LoginForm(forms.Form):
    password = PasswordField(
        label=_("Password"),
        autocomplete="current-password",
    )
    remember = forms.BooleanField(label=_("Remember Me"), required=False)

    user = None
    error_messages = {
        "account_inactive": _("This account is currently inactive."),
        "email_password_mismatch": _("The e-mail address and/or password you specified are not correct."),
        "username_password_mismatch": _("The username and/or password you specified are not correct."),
    }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(LoginForm, self).__init__(*args, **kwargs)
        if app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.EMAIL:
            login_widget = forms.TextInput(
                attrs={
                    "type": "email",
                    "placeholder": _("E-mail address"),
                    "autocomplete": "email",
                    "autofocus": True,
                }
            )
            login_field = forms.EmailField(label=_("Email"), widget=login_widget)
        elif app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.USERNAME:
            login_widget = forms.TextInput(attrs={"placeholder": _("Username"), "autocomplete": "username"})
            login_field = forms.CharField(
                label=_("Username"),
                widget=login_widget,
                max_length=get_username_max_length(),
            )
        else:
            assert app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.USERNAME_EMAIL
            login_widget = forms.TextInput(attrs={"placeholder": _("Username or e-mail"), "autocomplete": "email"})
            login_field = forms.CharField(label=pgettext("field label", "Login"), widget=login_widget)
        self.fields["login"] = login_field
        set_form_field_order(self, ["login", "password", "remember"])
        self.fields["remember"].widget.attrs.update({"class": "kmmrce-checkbox__input"})

        if app_settings.SESSION_REMEMBER is not None:
            del self.fields["remember"]

    def user_credentials(self):
        """
        Provides the credentials required to authenticate the user for
        login.
        """
        credentials = {}
        login = self.cleaned_data["login"]
        if app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.EMAIL:
            credentials["email"] = login
        elif app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.USERNAME:
            credentials["username"] = login
        else:
            if self._is_login_email(login):
                credentials["email"] = login
            credentials["username"] = login
        credentials["password"] = self.cleaned_data["password"]
        return credentials

    def clean_login(self):
        login = self.cleaned_data["login"]
        return login.strip()

    def _is_login_email(self, login):
        try:
            validators.validate_email(login)
            ret = True
        except exceptions.ValidationError:
            ret = False
        return ret

    def clean(self):
        super(LoginForm, self).clean()
        if self._errors:
            return
        credentials = self.user_credentials()
        user = get_adapter(self.request).authenticate(self.request, **credentials)
        if user:
            self.user = user
        else:
            auth_method = app_settings.AUTHENTICATION_METHOD
            if auth_method == app_settings.AuthenticationMethod.USERNAME_EMAIL:
                login = self.cleaned_data["login"]
                if self._is_login_email(login):
                    auth_method = app_settings.AuthenticationMethod.EMAIL
                else:
                    auth_method = app_settings.AuthenticationMethod.USERNAME
            raise forms.ValidationError(self.error_messages["%s_password_mismatch" % auth_method])
        return self.cleaned_data

    def login(self, request, redirect_url=None):
        email = self.user_credentials().get("email")
        ret = perform_login(
            request,
            self.user,
            email_verification=app_settings.EMAIL_VERIFICATION,
            redirect_url=redirect_url,
            email=email,
        )
        remember = app_settings.SESSION_REMEMBER
        if remember is None:
            remember = self.cleaned_data["remember"]
        if remember:
            request.session.set_expiry(app_settings.SESSION_COOKIE_AGE)
        else:
            request.session.set_expiry(0)
        return ret


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("First name"),
                "autofocus": True,
            }
        ),
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Last name"),
            }
        ),
    )

    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "placeholder": _("E-mail address"),
                "autocomplete": "email",
            }
        ),
    )

    password1 = SetPasswordField(
        label=_("Password"),
    )
    password2 = PasswordField(
        label=_("Confirm password"),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.pop("autofocus", None)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if self.Meta.model.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Email already exists."))
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.save()
        return user
