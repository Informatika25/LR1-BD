from django import forms
from .models import Reservation


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