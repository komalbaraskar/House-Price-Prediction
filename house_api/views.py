from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views import View
import joblib
import json
import os
import numpy as np
import pandas as pd

from mongo import predictions
from datetime import datetime


# 🏠 Home Page
def home(request):
    return render(request, 'home.html')


# 🧠 Paths for model and feature list
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'model', 'house_price_model.pkl')
features_path = os.path.join(BASE_DIR, 'model', 'features.json')

print("🔍 Checking model path:", model_path)

# ✅ Load the model
model = None
try:
    if os.path.exists(model_path) and os.path.getsize(model_path) > 0:
        model = joblib.load(model_path)
        print("✅ Model loaded successfully from:", model_path)
    else:
        print("⚠️ Model file missing or empty.")
except Exception as e:
    print("❌ Error loading model:", e)

# ✅ Load feature names
features = []
try:
    with open(features_path, 'r') as f:
        features = json.load(f)
    print("✅ Features loaded successfully:", features)
except Exception as e:
    print("⚠️ Could not load features:", e)


# 🧩 Simple GET test view
class PredictView(View):
    def get(self, request):
        return JsonResponse({
            "message": "✅ API is working! Use POST /api/predict/ to get house price predictions."
        })


# 🚀 Main Prediction API endpoint
@api_view(['POST'])
def predict_price(request):
    if model is None:
        return Response({'error': 'Model not loaded. Please check your model file.'}, status=500)

    try:
        data = request.data
        print("📦 Received data:", data)

        # Convert incoming JSON to DataFrame with correct feature order
        input_dict = {f: [float(data.get(f, 0))] for f in features}
        input_df = pd.DataFrame(input_dict)
        print("📊 Input DataFrame:")
        print(input_df)

        # Predict
        prediction = model.predict(input_df)[0]
        print("💰 Predicted price (raw):", prediction)

        # Convert to Indian Rupees (if model predicts in USD)
        conversion_rate = 83.0  # 1 USD ≈ ₹83 (you can update this dynamically)
        price_in_inr = prediction * conversion_rate

        print("🇮🇳 Predicted price in INR:", price_in_inr)

        # Return nicely formatted response
        return Response({
            'predicted_price_inr': f"₹{price_in_inr:,.2f}",
            'predicted_price_raw': round(float(price_in_inr), 2)
        })

    except Exception as e:
        print("❌ Prediction error:", e)
        return Response({'error': str(e)}, status=400)
