from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.PredictView.as_view(), name='predict'),
    path('medication-reminder/', views.MedicationReminderView.as_view(), name='medication-reminder'),
    path('symptom-report/', views.SymptomReportView.as_view(), name='symptom-report'),
]