# flake8: noqa

from django import forms

from dashboard.models import Dashboard


class CreateDashboardPublicationForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)
    upload_pdf = forms.FileField(required=True)


# class DashboardDeleteForm(forms.ModelForm):
#     class Meta:
#         model = Dashboard
#         exclude = ['field', 'publication']


# class EditDashboardFieldForm(forms.Form):
#     field = forms.CharField(max_length=128, required=True)
#     aoc = forms.CharField(
#         max_length=255, required=False,
#         help_text='area of concentration'
#     )
#
#     def clean(self):
#         pass


class AddDashboardFieldForm(forms.ModelForm):
    keyword = forms.CharField(max_length=128, required=True)
    aoc = forms.CharField(
        max_length=255, required=True,
        help_text='area of concentration'
    )

    class Meta:
        model = Dashboard
        exclude = ['publication', 'field']

    def clean(self):
        pass
