from django.db import models


class Prediction(models.Model):
    city = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    pm25 = models.FloatField()
    pm10 = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    asthma_risk = models.CharField(max_length=20)
    advice = models.TextField()

    def __str__(self):
        return f"{self.city} - {self.timestamp}"