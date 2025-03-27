from django.urls import path
from . import views
# from line_pdf.views import generate_pdf

urlpatterns = [
    path('contracts/', views.ContractInfoForm, name='ContractInfoForm'),
    # path('receipt/<int:payment_id>/', print_report, name='print_report'),
    
]