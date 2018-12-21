from refconn.models import MonthlyUsagePerCamp,RefugeeNationality,ApplicationUsage,Camp,Country,CampType,CampAdmin,Nationality,ApplicationCategory
from rest_framework import response, serializers, status


class CountrySerializer(serializers.ModelSerializer):

	class Meta:
		model = Country
		fields = ('country_id', 'country_name')


class CampAdminSerializer(serializers.ModelSerializer):

	class Meta:
		model = CampAdmin
		fields = ('camp_admin_id', 'camp_admin_name')

# class SubRegionSerializer(serializers.ModelSerializer):

# 	class Meta:
# 		model = SubRegion
# 		fields = ('sub_region_id', 'sub_region_name', 'region_id')


# class IntermediateRegionSerializer(serializers.ModelSerializer):

# 	class Meta:
# 		model = IntermediateRegion
# 		fields = ('intermediate_region_id', 'intermediate_region_name', 'sub_region_id')


class CampTypeSerializer(serializers.ModelSerializer):
	country = CountrySerializer(many=False, read_only=True)
	
	class Meta:
		model = CampType
		fields = ('camp_type_id', 'country', 'camp_type_name')


# class DevStatusSerializer(serializers.ModelSerializer):

# 	class Meta:
# 		model = DevStatus
# 		fields = ('dev_status_id', 'dev_status_name')


# class CountryAreaSerializer(serializers.ModelSerializer):
# 	dev_status = DevStatusSerializer(many=False, read_only=True)
# 	location = LocationSerializer(many=False, read_only=True)

# 	class Meta:
# 		model = CountryArea
# 		fields = (
# 			'country_area_id',
# 			'country_area_name',
# 			'm49_code',
# 			'iso_alpha3_code',
# 			'dev_status',
# 			'location')


# class HeritageSiteCategorySerializer(serializers.ModelSerializer):

# 	class Meta:
# 		model = HeritageSiteCategory
# 		fields = ('category_id', 'category_name')


# class HeritageSiteJurisdictionSerializer(serializers.ModelSerializer):
# 	heritage_site_id = serializers.ReadOnlyField(source='heritage_site.heritage_site_id')
# 	country_area_id = serializers.ReadOnlyField(source='country_area.country_area_id')

# 	class Meta:
# 		model = HeritageSiteJurisdiction
# 		fields = ('heritage_site_id', 'country_area_id')

class CampSerializer(serializers.ModelSerializer):
	camp_type = CampTypeSerializer(many=False, read_only=True)
	country = CountrySerializer(many=False, read_only=True)
	camp_admin = CampAdminSerializer(many=False, read_only=True)

	class Meta:
		model = Camp
		fields = (
			'camp_id',
			'camp_name',
			'country',
			'camp_admin',
			'camp_type',
			'latitude',
			'longitude',
			'bandwidth_down',
			'bandwidth_up')

class RefugeeNationalitySerializer(serializers.ModelSerializer):
	mupc_id = serializers.ReadOnlyField(source='monthly_usage_per_camp.mupc_id')
	nationality_id = serializers.ReadOnlyField(source='nationality.nationality_id')
	nationality_proportion = serializers.FloatField(allow_null=True)

	class Meta:
		model = RefugeeNationality
		fields = ('mupc_id','nationality_id','nationality_proportion')

class ApplicationUsageSerializer(serializers.ModelSerializer):
	mupc_id = serializers.ReadOnlyField(source='monthly_usage_per_camp.mupc_id')
	application_category_id = serializers.ReadOnlyField(source='application_category.application_category_id')
	total_usage_kb = serializers.FloatField(allow_null=True)

	class Meta:
		model = ApplicationUsage
		fields = ('mupc_id', 'application_category_id','total_usage_kb')

class MonthlyUsagePerCampSerializer(serializers.ModelSerializer):
	total_infrastructure_devices = serializers.IntegerField(
		allow_null=True
	)
	month_num = serializers.IntegerField(
		allow_null=True
	)
	year_num = serializers.IntegerField(
		allow_null=True
	)
	camp = CampSerializer(
		many=False,
		read_only=True
	)
	camp_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=Camp.objects.all(),
		source='camp'
	)
	refugee_nationality = RefugeeNationalitySerializer(
		source='refugee_nationality_set', # Note use of _set
		many=True,
		read_only=True
	)
	refugee_nationalities = serializers.ListField(
		write_only=True,
		source='refugee_nationality'
	)
	application_usage = ApplicationUsageSerializer(
		source='application_usage_set', # Note use of _set
		many=True,
		read_only=True
	)
	application_usages = serializers.ListField(
		write_only=True,
		source='application_usage'
	)

	class Meta:
		model = MonthlyUsagePerCamp
		fields = (
			'mupc_id',
			'camp_id',
			'camp',
			'total_infrastructure_devices',
			'month_num',
			'year_num',
			'refugee_nationality',
			'refugee_nationalities',
			'application_usage',
			'application_usages'
		)

	def create(self, validated_data):
		"""
		This method persists a new HeritageSite instance as well as adds all related
		countries/areas to the heritage_site_jurisdiction table.  It does so by first
		removing (validated_data.pop('heritage_site_jurisdiction')) from the validated
		data before the new HeritageSite instance is saved to the database. It then loops
		over the heritage_site_jurisdiction array in order to extract each country_area_id
		element and add entries to junction/associative heritage_site_jurisdiction table.
		:param validated_data:
		:return: site
		"""

		print(validated_data)

		nationalities = validated_data.pop('refugee_nationality')
		categories = validated_data.pop('application_usage')
		mupc = MonthlyUsagePerCamp.objects.create(**validated_data)

		if nationalities is not None:
			for nat in nationalities:
				RefugeeNationality.objects.create(
					mupc_id=mupc.mupc_id,
					nationality_id=nat['nationality_id'],
					nationality_proportion=nat['nationality_proportion']
				)
		if categories is not None:
			for cat in categories:
				ApplicationUsage.objects.create(
					mupc_id=mupc.mupc_id,
					application_category_id=cat['application_category_id'],
					total_usage_kb=cat['total_usage_kb']
				)
		return mupc

	def update(self, instance, validated_data):
		# site_id = validated_data.pop('heritage_site_id')
		mupc_id = instance.mupc_id
		new_nationalities = validated_data.pop('refugee_nationality')
		new_categories = validated_data.pop('application_usage')

		instance.total_infrastructure_devices = validated_data.get(
			'total_infrastructure_devices',
			instance.total_infrastructure_devices
		)
		instance.month_num = validated_data.get(
			'month_num',
			instance.month_num
		)
		instance.year_num = validated_data.get(
			'year_num',
			instance.year_num
		)
		instance.camp_id = validated_data.get(
			'camp_id',
			instance.camp_id
		)
		instance.save()

		# TODO BOTH OF THE CHECKS BELOW NEED TO CHECK TWO PROPERTY VALUES
		# For refugee nationalities, if the nationality is unchanged but the nationality proportion
		# has changed then update.
		# For app categories, if the app category is unchanged but the total usage in kb has
		# changed, then update.

		# If any existing nationalities are not in updated list, delete them
		new_ids = []
		old_ids = RefugeeNationality.objects \
			.values_list('nationality_id', flat=True) \
			.filter(mupc_id__exact=mupc_id)

		# Insert new unmatched country entries
		for nat in new_nationalities:
			new_id = nat['nationality_id']
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				RefugeeNationality.objects.create(
					mupc_id=mupc_id,
					nationality_id=new_id,
					nationality_proportion=nat['nationality_proportion']
				)

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				RefugeeNationality.objects.filter(
					mupc_id=mupc_id,
					nationality_id=old_id
				).delete()

		new_category_ids = []
		old_category_ids = ApplicationUsage.objects.values_list(
			'application_category_id', flat=True
		).filter(mupc_id__exact=mupc_id)

		# Insert new unmatched category entries
		for category in new_categories:
			new_id = category['application_category_id']
			new_category_ids.append(new_id)
			if new_id in old_category_ids:
				continue
			else:
				ApplicationUsage.objects.create(
					mupc_id=mupc_id,
					application_category_id=new_id,
					total_usage_kb=category['total_usage_kb']
				)

		# Delete old unmatched country entries
		for old_id in old_category_ids:
			if old_id in new_category_ids:
				continue
			else:
				ApplicationUsage.objects.filter(
					mupc_id=mupc_id,
					application_category_id=old_id
				).delete()

		return instance
