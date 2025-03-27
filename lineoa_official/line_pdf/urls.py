from django.urls import path
from .views import generate_pdf

urlpatterns = [
    path('receipt/', generate_pdf, name='receipt'),
]
