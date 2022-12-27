from django.forms import ModelForm, DateInput
from cal.models.event import Event
from django import forms


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "start_time", "end_time", "description"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter event title",
                },
            ),
            "start_time": DateInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                    "placeholder": "Start Time 'Y-m-d H:M:S'",
                },
                format="%Y-%m-%dT%H:%M"
            ),
            "end_time": DateInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                    "placeholder": "End Time 'Y-m-d H:M:S'",
                },
                format="%Y-%m-%dT%H:%M"
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter event description",
                },
            ),
        }
        #exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["title"].label = ""
        self.fields["start_time"].label = ""
        self.fields["end_time"].label = ""
        self.fields["description"].label = ""
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M")
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M")
