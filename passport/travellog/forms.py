from django import forms
from .models import Destination, JournalEntry

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ["country", "city", "visited", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ["city", "rating", "notes", "image"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
        }