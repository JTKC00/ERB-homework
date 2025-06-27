from django import forms
from .models import Meeting, AgendaItem

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['title', 'date', 'start_time', 'end_time', 'location', 'attendees', 'minutes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class AgendaItemForm(forms.ModelForm):
    class Meta:
        model = AgendaItem
        fields = ['item_title', 'description', 'responsible_person', 'estimated_time']