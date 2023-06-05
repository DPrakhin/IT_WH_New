from django import forms
from .models import RequestDevice


class ItemForm(forms.ModelForm):
    class Meta:
        model = RequestDevice
        fields = ('user', 'employee', 'item', 'notes')