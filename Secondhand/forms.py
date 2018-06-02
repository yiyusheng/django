from django import forms
from Secondhand import models

class wordSubscribeForm(forms.ModelForm):
    class Meta:
        model = models.WordSubscribe
        fields = ['user','sckey','word']
