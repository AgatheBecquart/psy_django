from django import forms

class PatientTextEntryForm(forms.Form):
    text = forms.CharField(label='Text', widget=forms.Textarea)
