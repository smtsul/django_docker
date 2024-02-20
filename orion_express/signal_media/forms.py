from django import forms

class SettingForm(forms.Form):
    setting_content = forms.CharField(widget=forms.Textarea)


class YearForm(forms.Form):
    year = forms.CharField(max_length=4, required=True)

