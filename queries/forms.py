from django import forms

from .models import Query


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = "__all__"


class SearchForm(forms.Form):

    query = forms.CharField()
    timeout = forms.FloatField(min_value=0.0, required=False)
    browser = forms.ChoiceField(choices=(('Chrome', 'Chrome'), ('Firefox', 'Firefox')), initial='Firefox')
    proxy = forms.GenericIPAddressField(required=False)
