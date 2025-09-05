from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "username",
            "email",
            "full_name",
            "phone",
            "address",
            "profile_photo",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Crispy Forms Helper
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.enctype = "multipart/form-data"  # allow file upload
        self.helper.label_class = "fw-bold"  # Bootstrap bold labels
        self.helper.field_class = "mb-3"  # spacing between fields

        # Layout definition
        self.helper.layout = Layout(
            Row(
                Column("username", css_class="col-md-6"),
                Column("email", css_class="col-md-6"),
            ),
            "full_name",
            Row(
                Column("phone", css_class="col-md-6"),
                Column("address", css_class="col-md-6"),
            ),
            "profile_photo",
            Row(
                Column("password1", css_class="col-md-6"),
                Column("password2", css_class="col-md-6"),
            ),
            Submit("submit", "Sign Up", css_class="btn btn-success w-100"),
        )


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_show_labels = True
        self.helper.label_class = "fw-bold"
        self.helper.field_class = "mb-3"

        self.helper.layout = Layout(
            Field("username", placeholder="Enter your username"),
            Field("password", placeholder="Enter your password"),
            Submit("login", "Log In", css_class="btn btn-primary w-100"),
        )
