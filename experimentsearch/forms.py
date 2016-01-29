import datetime

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from mongcore.models import ExperimentForTable


class SearchTypeSelect(forms.Form):
    parameters = (
        (ExperimentForTable.field_names[0], ExperimentForTable.field_names[0]),
        (ExperimentForTable.field_names[1], ExperimentForTable.field_names[1]),
        (ExperimentForTable.field_names[2], ExperimentForTable.field_names[2]),
        ("Advanced Search", "Advanced Search")
    )
    search_by = forms.ChoiceField(
        parameters, label='Search by', required=False,
        widget=forms.Select(attrs={"onChange": 'this.form.submit()'})
    )


class NameSearchForm(forms.Form):
    search_name = forms.CharField(
        max_length=200, label='',
        widget=forms.TextInput(attrs={"class": "search_field"})
    )


class PISearchForm(forms.Form):
    search_pi = forms.CharField(
        max_length=200, label='',
        widget=forms.TextInput(attrs={"class": "search_field"})
    )


class DateSearchForm(forms.Form):
    current_year = datetime.datetime.now().year
    years = []
    for year in range(2013, current_year+1):
        years.append(year)
    from_date = forms.DateTimeField(
        label='From ', widget=SelectDateWidget(years=years),
    )
    to_date = forms.DateTimeField(
        label=' To ', widget=SelectDateWidget(years=years),
    )

    def clean(self):
        cleaned_data = super(DateSearchForm, self).clean()
        if cleaned_data.get('to_date') < cleaned_data.get('from_date'):
            raise forms.ValidationError(
                "Date to search from must precede date to search to"
            )


class AdvancedSearchForm(forms.Form):
    search_name = forms.CharField(
        max_length=200, label=ExperimentForTable.field_names[0],
        widget=forms.TextInput(attrs={"class": "search_input"}),
        required=False
    )

    search_pi = forms.CharField(
        max_length=200, label=ExperimentForTable.field_names[1],
        widget=forms.TextInput(attrs={"class": "search_input"}),
        required=False
    )

    current_year = datetime.datetime.now().year
    years = []
    for year in range(2013, current_year+1):
        years.append(year)
    from_date = forms.DateTimeField(
        label='From ', widget=SelectDateWidget(years=years, attrs={"class": "search_input"}),
        required=False
    )
    to_date = forms.DateTimeField(
        label=' To ', widget=SelectDateWidget(years=years, attrs={"class": "search_input"}),
        required=False
    )

    def clean(self):
        cleaned_data = super(AdvancedSearchForm, self).clean()
        todate = cleaned_data.get('to_date')
        fromdate = cleaned_data.get('from_date')
        if todate and fromdate and todate < fromdate:
            raise forms.ValidationError(
                "Date to search from must precede date to search to"
            )
