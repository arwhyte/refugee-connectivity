from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse,reverse_lazy
from django_filters.views import FilterView
from django.db.models import Q
from .models import Camp,MonthlyUsagePerCamp,RefugeeNationality,CampDemographics,ApplicationUsage,DailyUsagePerCamp
from .forms import CampForm # added manually 
from .filters import MupcFilter,DupcFilter


def index(request):
	return HttpResponse("Hello, world. You're at the Refugee Connectivity index page.")


class AboutPageView(generic.TemplateView):
	template_name = 'refconn/about.html'


class HomePageView(generic.TemplateView):
	template_name = 'refconn/home.html'


class CampListView(generic.ListView):
	model = Camp
	context_object_name = 'camps' # in the template html in {} for the python code, this is what refers to the model
	template_name = 'refconn/camps.html'
	paginate_by = 20

	def get_queryset(self):
		return Camp.objects.all().order_by('camp_name') 

@method_decorator(login_required, name='dispatch')
class CampDetailView(generic.DetailView):
	model = Camp
	context_object_name = 'camp'
	template_name = 'refconn/camp_detail.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

@method_decorator(login_required, name='dispatch')
class CampCreateView(generic.View):
	model = Camp
	form_class = CampForm
	success_message = "Refugee Camp created successfully"
	template_name = 'refconn/camp_new.html'
	# fields = '__all__' <-- superseded by form_class
	# success_url = reverse_lazy('heritagesites/site_list')

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = CampForm(request.POST)
		if form.is_valid():
			camp = form.save(commit=False)
			camp.save()
			# return redirect(site) # shortcut to object's get_absolute_url()
			return HttpResponseRedirect(camp.get_absolute_url())
		return render(request, 'refconn/camp_new.html', {'form': form})

	def get(self, request):
		form = CampForm()
		return render(request, 'refconn/camp_new.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class CampUpdateView(generic.UpdateView):
	model = Camp
	form_class = CampForm
	# fields = '__all__' <-- superseded by form_class
	context_object_name = 'camp'
	# pk_url_kwarg = 'site_pk'
	success_message = "Refugee Camp updated successfully"
	template_name = 'refconn/camp_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		camp = form.save(commit=False)
		# site.updated_by = self.request.user
		# site.date_updated = timezone.now()
		camp.save()

		return HttpResponseRedirect(camp.get_absolute_url())
		# return redirect('heritagesites/site_detail', pk=site.pk)

@method_decorator(login_required, name='dispatch')
class CampDeleteView(generic.DeleteView):
	model = Camp
	success_message = "Refugee Camp deleted successfully"
	success_url = reverse_lazy('camps')
	context_object_name = 'camp'
	template_name = 'refconn/camp_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete CampDem entries
		CampDemographics.objects.select_related('mupc') \
			.filter(Q(mupc__camp__camp_id=self.object.camp_id)) \
			.delete()
		# Delete refugee_nat entries
		RefugeeNationality.objects.select_related('mupc') \
			.filter(Q(mupc__camp__camp_id=self.object.camp_id)) \
			.delete()
		# Delete app_u entries
		ApplicationUsage.objects.select_related('mupc') \
			.filter(Q(mupc__camp__camp_id=self.object.camp_id)) \
			.delete()
		# Delete daily_u entries
		DailyUsagePerCamp.objects.select_related('mupc') \
			.filter(Q(mupc__camp__camp_id=self.object.camp_id)) \
			.delete()
		# Delete monthly_u entries
		MonthlyUsagePerCamp.objects.select_related('camp') \
			.filter(Q(camp__camp_id=self.object.camp_id)) \
			.delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())

class MupcFilterView(FilterView):
	filterset_class = MupcFilter
	template_name = 'refconn/mupc_filter.html'

class DupcFilterView(FilterView):
	filterset_class = DupcFilter
	template_name = 'refconn/dupc_filter.html'

@method_decorator(login_required, name='dispatch')
class MupcDetailView(generic.DetailView):
	model = MonthlyUsagePerCamp
	context_object_name = 'mupc'
	template_name = 'refconn/mupc_detail.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

@method_decorator(login_required, name='dispatch')
class DupcDetailView(generic.DetailView):
	model = DailyUsagePerCamp
	context_object_name = 'dupc'
	template_name = 'refconn/dupc_detail.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

# @method_decorator(login_required, name='dispatch')
# class CountryAreaListView(generic.ListView):
# 	model = CountryArea
# 	context_object_name = 'countries'
# 	template_name = 'heritagesites/country_area.html'
# 	paginate_by = 20

# 	def dispatch(self, *args, **kwargs):
# 		return super().dispatch(*args, **kwargs)

# 	def get_queryset(self):
# 		# return CountryArea.objects.all().order_by('country_area_name')
# 		return CountryArea.objects.all().select_related('dev_status','location').order_by('country_area_name')

# @method_decorator(login_required, name='dispatch')
# class CountryAreaDetailView(generic.DetailView):
# 	model = CountryArea
# 	context_object_name = 'country'
# 	template_name = 'heritagesites/country_area_detail.html'
# 	def dispatch(self, *args, **kwargs):
# 		return super().dispatch(*args, **kwargs)

# @method_decorator(login_required, name='dispatch')
# class SiteCreateView(generic.View):
# 	model = HeritageSite
# 	form_class = HeritageSiteForm
# 	success_message = "Heritage Site created successfully"
# 	template_name = 'heritagesites/site_new.html'
# 	# fields = '__all__' <-- superseded by form_class
# 	# success_url = reverse_lazy('heritagesites/site_list')

# 	def dispatch(self, *args, **kwargs):
# 		return super().dispatch(*args, **kwargs)

# 	def post(self, request):
# 		form = HeritageSiteForm(request.POST)
# 		if form.is_valid():
# 			site = form.save(commit=False)
# 			site.save()
# 			for country in form.cleaned_data['country_area']:
# 				HeritageSiteJurisdiction.objects.create(heritage_site=site, country_area=country)
# 			# return redirect(site) # shortcut to object's get_absolute_url()
# 			return HttpResponseRedirect(site.get_absolute_url())
# 		return render(request, 'heritagesites/site_new.html', {'form': form})

# 	def get(self, request):
# 		form = HeritageSiteForm()
# 		return render(request, 'heritagesites/site_new.html', {'form': form})

# @method_decorator(login_required, name='dispatch')
# class SiteUpdateView(generic.UpdateView):
# 	model = HeritageSite
# 	form_class = HeritageSiteForm
# 	# fields = '__all__' <-- superseded by form_class
# 	context_object_name = 'site'
# 	# pk_url_kwarg = 'site_pk'
# 	success_message = "Heritage Site updated successfully"
# 	template_name = 'heritagesites/site_update.html'

# 	def dispatch(self, *args, **kwargs):
# 		return super().dispatch(*args, **kwargs)

# 	def form_valid(self, form):
# 		site = form.save(commit=False)
# 		# site.updated_by = self.request.user
# 		# site.date_updated = timezone.now()
# 		site.save()

# 		# Current country_area_id values linked to site
# 		old_ids = HeritageSiteJurisdiction.objects\
# 			.values_list('country_area_id', flat=True)\
# 			.filter(heritage_site_id=site.heritage_site_id)

# 		# New countries list
# 		new_countries = form.cleaned_data['country_area']

# 		# TODO can these loops be refactored?

# 		# New ids
# 		new_ids = []

# 		# Insert new unmatched country entries
# 		for country in new_countries:
# 			new_id = country.country_area_id
# 			new_ids.append(new_id)
# 			if new_id in old_ids:
# 				continue
# 			else:
# 				HeritageSiteJurisdiction.objects \
# 					.create(heritage_site=site, country_area=country)

# 		# Delete old unmatched country entries
# 		for old_id in old_ids:
# 			if old_id in new_ids:
# 				continue
# 			else:
# 				HeritageSiteJurisdiction.objects \
# 					.filter(heritage_site_id=site.heritage_site_id, country_area_id=old_id) \
# 					.delete()

# 		return HttpResponseRedirect(site.get_absolute_url())
# 		# return redirect('heritagesites/site_detail', pk=site.pk)

# @method_decorator(login_required, name='dispatch')
# class SiteDeleteView(generic.DeleteView):
# 	model = HeritageSite
# 	success_message = "Heritage Site deleted successfully"
# 	success_url = reverse_lazy('site')
# 	context_object_name = 'site'
# 	template_name = 'heritagesites/site_delete.html'

# 	def dispatch(self, *args, **kwargs):
# 		return super().dispatch(*args, **kwargs)

# 	def delete(self, request, *args, **kwargs):
# 		self.object = self.get_object()

# 		# Delete HeritageSiteJurisdiction entries
# 		HeritageSiteJurisdiction.objects \
# 			.filter(heritage_site_id=self.object.heritage_site_id) \
# 			.delete()

# 		self.object.delete()

# 		return HttpResponseRedirect(self.get_success_url())