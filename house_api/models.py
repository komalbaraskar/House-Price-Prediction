from django.db import models

# This app does not require DB models for prediction API, but placeholder if you want to store requests
class Prediction(models.Model):
    input_json = models.JSONField()
    predicted_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction {self.id} - {self.predicted_price}"
