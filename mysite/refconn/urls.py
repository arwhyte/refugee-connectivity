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
    path('camps/new/', views.CampCreateView.as_view(), name='camp_new'),
    path('camps/<int:pk>/delete/', views.CampDeleteView.as_view(), name='camp_delete'),
    path('camps/<int:pk>/update/', views.CampUpdateView.as_view(), name='camp_update'),
    path('camps/<int:pk>/', views.CampDetailView.as_view(), name='camp_detail'),
    path('monthly/',views.MupcFilterView.as_view(), name='mupc_filter'),
    path('daily/', views.DupcFilterView.as_view(), name='dupc_filter'),
    path('monthly/<int:pk>/', views.MupcDetailView.as_view(), name='mupc_detail'),
    path('daily/<int:pk>/', views.DupcDetailView.as_view(), name='dupc_detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL},name='logout'),
]