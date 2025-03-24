from django.urls import path
from . import views
from line_pdf.views import print_report

urlpatterns = [
    path('contracts/', views.ContractInfoForm, name='ContractInfoForm'),
    # path('receipt/<int:payment_id>/', print_report, name='print_report'),
    
]