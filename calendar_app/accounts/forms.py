from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from accounts.models import User

class SignInForm(forms.Form):
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address"}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}))


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
        validators=[validate_password],
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Repeat Password"}),
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ["email"]
        widgets = {"email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address"})}

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password didn't match!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["email"].label = ""
