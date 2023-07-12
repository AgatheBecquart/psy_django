from django import forms
from authentication.models import Patient

class PatientTextEntryForm(forms.Form):
    text = forms.CharField(label='Text', widget=forms.Textarea)
    

    