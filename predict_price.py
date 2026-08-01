import joblib
import json
import pandas as pd
import os
import traceback
from mongo import predictions
from datetime import datetime

try:
    model_path = os.path.join('model', 'house_price_model.pkl')
    features_path = os.path.join('model', 'features.json')

    model = joblib.load(model_path)
    with open(features_path, 'r') as f:
        features = json.load(f)

    print("✅ Model and features loaded successfully:", features)

    new_house = {
        "sqft": 2000,
        "bedrooms": 3,
        "bathrooms": 2,
        "zipcode": 2139,
        "year_built": 2010
    }

    input_df = pd.DataFrame([new_house])[features]
    print("\n📊 Input DataFrame:")
    print(input_df)

    predicted_price = model.predict(input_df)[0]
    predictions.insert_one({
        "input_data": new_house,
        "predicted_price": float(predicted_price),
        "created_at": datetime.now()
    })
    print(f"\n💰 Predicted house price: ${predicted_price:,.2f}")
    print("✅ Prediction saved to MongoDB")
    
except Exception as e:
    print("❌ Prediction error:", e)
    traceback.print_exc()
