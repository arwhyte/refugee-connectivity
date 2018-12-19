from django.contrib import admin

import refconn.models as models

# @admin.register(models.ApplicationCategory)
# class ApplicationCategoryAdmin(admin.ModelAdmin):
# 	fields = ['application_category_name']
# 	list_display = ['application_category_name']
# 	ordering = ['application_category_name']

# app_u will be filled out in the monthly usage

@admin.register(models.Camp)
class Camp(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': (
				'camp_name',
				'camp_admin',
				'camp_type',
			)
		}),
		('Location', {
			'fields': [
				(
					'country',
					'longitude',
					'latitude'
				)
			]
		}),
		('Bandwidth', {
			'fields': [
				(
					'bandwidth_up',
					'bandwidth_down'
				)
			]
		})
	)

	list_filter = (
		'country',
		'camp_type',
		'camp_admin'
	)

# @admin.register(models.CampAdmin)
# class CampAdminAdmin(admin.ModelAdmin):
# 	fields = ['camp_admin_name']
# 	list_display = ['camp_admin_name']
# 	ordering = ['camp_admin_name']

