from django import forms

from publication.models import Publication


class AddPublicationForm(forms.ModelForm):

    class Meta:
        model = Publication
        exclude = ['author', 'id']
