import django_filters
from refconn.models import MonthlyUsagePerCamp,DailyUsagePerCamp,Country


class MupcFilter(django_filters.FilterSet):
	camp_name = django_filters.CharFilter(
		field_name='camp__camp_name',
		label='Refugee Camp Name',
		lookup_expr='icontains'
	)

	country = django_filters.ModelChoiceFilter(
		field_name='camp__country__country_name',
		label='Country',
		queryset=Country.objects.all().order_by('country_name'),
		lookup_expr='exact'
	)

	month = django_filters.NumberFilter(
		field_name='month_num',
		label='Month',
		lookup_expr='exact'
	)

	year = django_filters.NumberFilter(
		field_name='year_num',
		label='Year',
		lookup_expr='exact'
	)


	class Meta:
		model = MonthlyUsagePerCamp
		# form = SearchForm
		# fields [] is required, even if empty.
		fields = []

class DupcFilter(django_filters.FilterSet):
	camp_name = django_filters.CharFilter(
		field_name='mupc__camp__camp_name',
		label='Refugee Camp Name',
		lookup_expr='icontains'
	)

	country = django_filters.ModelChoiceFilter(
		field_name='mupc__camp__country__country_name',
		label='Country',
		queryset=Country.objects.all().order_by('country_name'),
		lookup_expr='exact'
	)

	date_field = django_filters.DateFilter(
		field_name='date_field',
		label='Date (YYYY-MM-DD)',
		lookup_expr='exact'
	)

	
	class Meta:
		model = DailyUsagePerCamp
		# form = SearchForm
		# fields [] is required, even if empty.
		fields = []