from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "username",
            "email",
            "full_name",
            "phone",
            "governorate",
            "address",
            "profile_photo",
            "password1",
            "password2",
        )
        widgets = {
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "type": "tel",
                    "placeholder": "100 123 4567",  # local number only
                }
            ),
        }
        help_texts = {
            "username": "Pick a unique username for your account.",
            "email": "We’ll send adoption updates to this email.",
            "phone": "Enter your full phone number (choose country code from dropdown).",
            "address": "Your home address helps us schedule home visits.",
            "profile_photo": "Upload a clear photo of yourself (optional).",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.enctype = "multipart/form-data"
        self.helper.label_class = "fw-bold"
        self.helper.field_class = "mb-3"

        self.helper.layout = Layout(
            Row(
                Column("username", css_class="col-md-6"),
                Column("email", css_class="col-md-6"),
            ),
            "full_name",
            Row(
                Column("phone", css_class="col-md-6"),
                Column("governorate", css_class="col-md-6"),
            ),
            "address",
            "profile_photo",
            Row(
                Column("password1", css_class="col-md-6"),
                Column("password2", css_class="col-md-6"),
            )
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
        )
