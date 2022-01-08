from django import forms
from .models import Event
from allauth.account.forms import SignupForm

from django.contrib.auth import get_user_model

User = get_user_model()


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = (
            "like_people",
            "created_by",
            "slug",
        )
        widgets = {
            "time": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
            ),
        }


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        label="First Name",
        widget=forms.TextInput(attrs={"placeholder": "First Name"}),
    )
    last_name = forms.CharField(
        max_length=30,
        label="Last Name",
        widget=forms.TextInput(attrs={"placeholder": "Last Name"}),
    )

    def signup(self, request, user):
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]
