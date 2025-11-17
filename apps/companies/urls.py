from django.urls import path
from .views import CompanyCreditView

urlpatterns = [
    path('score/', CompanyCreditView.as_view(), name='company-score'),
]