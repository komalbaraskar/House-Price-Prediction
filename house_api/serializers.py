from rest_framework import serializers

class PredictSerializer(serializers.Serializer):
sqft = serializers.FloatField(required=False)
bedrooms = serializers.FloatField(required=False)
bathrooms = serializers.FloatField(required=False)
zipcode = serializers.CharField(required=False, allow_blank=True)
age = serializers.FloatField(required=False)


def validate(self, data):
if not data:
raise serializers.ValidationError('No features provided')
return data