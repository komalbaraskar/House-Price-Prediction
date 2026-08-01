from django.contrib import admin
from django.urls import path, include
from house_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('house_api.urls')),  
    path('', views.home, name='home'),
]
