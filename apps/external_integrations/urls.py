from django.urls import path
from .views import SoliqRetrieveView, KadastrRetrieveView

urlpatterns = [
    path('soliq/<str:inn>/', SoliqRetrieveView.as_view(), name='external-soliq'),
    path('kadastr/<str:parcel_id>/', KadastrRetrieveView.as_view(), name='external-kadastr'),
]