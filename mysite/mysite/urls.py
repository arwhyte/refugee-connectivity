from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('refconn/', include('refconn.urls')),
    path('admin/', admin.site.urls),
]