import datetime

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from mongcore.models import ExperimentForTable


class SearchTypeSelect(forms.Form):
    """
    Drop down box for selecting what field the user wants to query the database by
    """
    parameters = (
        ("Experiment", "Experiment"),
        ("Data Source", "DataSource"),
        ("Term","Term"),
        ("Genotype","Genotype")
    )
    search_by = forms.ChoiceField(
        parameters, label='Search by', required=False
        #widget=forms.Select(attrs={"onChange": 'this.form.submit()'})
    )


class NameSearchForm(forms.Form):
    search_name = forms.CharField(
        max_length=200, label='', required=True,
        widget=forms.TextInput(attrs={"class": "search_field"})
    )


class PISearchForm(forms.Form):
    search_pi = forms.CharField(
        max_length=200, label='', required=True,
        widget=forms.TextInput(attrs={"class": "search_field"})
    )


class DateSearchForm(forms.Form):
    """
    Form for querying the database by date created. Has a field for date to search
    from, returning experiments created after the inputted date. Has a field for date to
    search to, returning experiments created before the inputted date. Both fields can be
    used to define a range of dates to query the database with
    """
    current_year = datetime.datetime.now().year
    years = []
    for year in range(2013, current_year+1):
        years.append(year)
    from_date = forms.DateTimeField(
        label='From ', widget=SelectDateWidget(years=years), required=False
    )
    to_date = forms.DateTimeField(
        label=' To ', widget=SelectDateWidget(years=years), required=False
    )

    def clean(self):
        """
        Checks if the form is valid by making sure at least one date has been completely
        filled and, if there are both dates, that the 'from' date precedes the 'to' date
        :return:
        """
        cleaned_data = super(DateSearchForm, self).clean()
        todate = cleaned_data.get('to_date')
        fromdate = cleaned_data.get('from_date')
        if not todate and not fromdate:
            raise forms.ValidationError(
                "Form must have at least one complete date"
            )
        if todate and fromdate and todate < fromdate:
            raise forms.ValidationError(
                "Date to search from must precede date to search to"
            )


class AdvancedSearchForm(forms.Form):
    """
    Form that allows for combining queries by name, primary investigator and date created
    """
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
