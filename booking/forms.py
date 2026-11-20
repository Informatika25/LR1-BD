from django import forms
from .models import Reservation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ("equipment", "start", "end", "purpose")
        labels = {
            "equipment": "Оборудование",
            "start": "Начало бронирования",
            "end": "Окончание бронирования",
            "purpose": "Цель использования",
        }
        widgets = {
            "start": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

        self.fields["username"].widget.attrs.update({
            "placeholder": "Придумайте имя пользователя",
            "autofocus": "autofocus",
        })
        self.fields["password1"].widget.attrs.update({
            "placeholder": "Введите пароль",
            "autocomplete": "new-password",
        })
        self.fields["password2"].widget.attrs.update({
            "placeholder": "Повторите пароль",
            "autocomplete": "new-password",
        })