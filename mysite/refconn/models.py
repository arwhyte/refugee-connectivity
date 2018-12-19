# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse


class ApplicationCategory(models.Model):
    application_category_id = models.AutoField(primary_key=True)
    application_category_name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'application_category'

    def __str__(self):
        return self.application_category_name

class Nationality(models.Model):
    nationality_id = models.AutoField(primary_key=True)
    nationality_name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'nationality'
    def __str__(self):
        return self.nationality_name



class Camp(models.Model):
    camp_id = models.AutoField(primary_key=True)
    camp_name = models.CharField(unique=True, max_length=45)
    country = models.ForeignKey('Country', models.DO_NOTHING, blank=True, null=True)
    camp_admin = models.ForeignKey('CampAdmin', models.DO_NOTHING, blank=True, null=True)
    camp_type = models.ForeignKey('CampType', models.DO_NOTHING, blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    bandwidth_up = models.FloatField(blank=True, null=True)
    bandwidth_down = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'camp'
        verbose_name = 'Refugee Camp'
        verbose_name_plural = 'Refugee Camps'
    def __str__(self):
        return self.camp_name
    def get_absolute_url(self):
        # return reverse('site_detail', args=[str(self.id)])
        return reverse('camp_detail', kwargs={'pk': self.pk})
    

class MonthlyUsagePerCamp(models.Model):
    mupc_id = models.AutoField(primary_key=True)
    camp = models.ForeignKey(Camp, models.DO_NOTHING)
    total_infrastructure_devices = models.IntegerField()
    month_num = models.IntegerField(blank=True, null=True)
    year_num = models.IntegerField(blank=True, null=True)

    nationality = models.ManyToManyField(Nationality, through='RefugeeNationality')
    application_category = models.ManyToManyField(ApplicationCategory, through='ApplicationUsage')

    class Meta:
        managed = False
        db_table = 'monthly_usage_per_camp'
        verbose_name = 'Monthly Data Usage Summary'

class ApplicationUsage(models.Model):
    appu_id = models.AutoField(primary_key=True)
    mupc = models.ForeignKey('MonthlyUsagePerCamp', models.DO_NOTHING)
    application_category = models.ForeignKey(ApplicationCategory, models.DO_NOTHING, blank=True, null=True)
    total_usage_kb = models.FloatField(db_column='total_usage_kB', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'application_usage'


class CampAdmin(models.Model):
    camp_admin_id = models.AutoField(primary_key=True)
    camp_admin_name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'camp_admin'
    def __str__(self):
        return self.camp_admin_name


class CampDemographics(models.Model):
    camp_dem_id = models.AutoField(primary_key=True)
    mupc = models.ForeignKey('MonthlyUsagePerCamp', models.DO_NOTHING)
    camp_population = models.IntegerField(blank=True, null=True)
    camp_capacity = models.FloatField(blank=True, null=True)
    adultmale = models.FloatField(blank=True, null=True)
    adultfemale = models.FloatField(blank=True, null=True)
    children = models.FloatField(blank=True, null=True)
    overcapacity = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'camp_demographics'
        verbose_name = 'Camp Demgraphics Information'


class CampType(models.Model):
    camp_type_id = models.AutoField(primary_key=True)
    camp_type_name = models.CharField(unique=True, max_length=45)
    country = models.ForeignKey('Country', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'camp_type'
    def __str__(self):
        return self.camp_type_name


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'country'
    def __str__(self):
        return self.country_name


class DailyUsagePerCamp(models.Model):
    dupc_id = models.AutoField(primary_key=True)
    mupc = models.ForeignKey('MonthlyUsagePerCamp', models.DO_NOTHING, blank=True, null=True)
    date_field = models.DateField(db_column='date_field', blank=True, null=True)  # Field renamed because it ended with '_'.
    total_clients = models.IntegerField(blank=True, null=True)
    total_usage_kb = models.FloatField(db_column='total_usage_kb',blank=True,null=True)

    class Meta:
        managed = False
        db_table = 'daily_usage_per_camp'



class RefugeeNationality(models.Model):
    ref_nat_id = models.AutoField(primary_key=True)
    mupc = models.ForeignKey(MonthlyUsagePerCamp, models.DO_NOTHING)
    nationality = models.ForeignKey(Nationality, models.DO_NOTHING)
    nationality_proportion = models.FloatField()

    class Meta:
        managed = False
        db_table = 'refugee_nationality'
