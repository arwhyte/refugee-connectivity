from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('camps/', views.CampListView.as_view(), name='camps'),
    path('monthly/', views.CampListView.as_view(), name='mupc_filter'),
    path('daily/', views.CampListView.as_view(), name='dupc_filter'),
    path('new/', views.CampListView.as_view(), name='camp_new'),
    path('camps/<int:pk>/', views.CampDetailView.as_view(), name='camp_detail'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL},name='logout'),
]