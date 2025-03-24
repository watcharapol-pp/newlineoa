from django.urls import path
from .views import print_report

urlpatterns = [
    path('receipt/', print_report, name='receipt_pdf'),
]
