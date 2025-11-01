from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('city', 'timestamp', 'asthma_risk')
    list_filter = ('asthma_risk', 'timestamp')
    search_fields = ('city',)