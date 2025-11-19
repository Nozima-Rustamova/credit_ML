from django.urls import path
from .views import CreditRequestListCreateView, CreditRequestDetailView

urlpatterns = [
    path('', CreditRequestListCreateView.as_view(), name='creditrequest-list-create'),
    path('<int:pk>/', CreditRequestDetailView.as_view(), name='creditrequest-detail'),
]