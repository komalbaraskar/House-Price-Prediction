from django.urls import path
from .views import home, predict_price
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('predict/', views.predict_price, name='predict_price'),
]

