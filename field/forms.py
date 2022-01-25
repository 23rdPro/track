from django import forms

from field.models import Field


class CreateFieldForm(forms.ModelForm):
    class Meta:
        model = Field
        exclude = ['guide', ]
