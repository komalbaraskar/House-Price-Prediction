import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import json
import os
from math import sqrt

data_path = os.path.join('data', 'houses.csv')
df = pd.read_csv(data_path)

target = 'price'
features = ['sqft', 'bedrooms', 'bathrooms', 'zipcode', 'year_built']

X = df[features]
y = df[target]

categorical_features = ['zipcode']
numeric_features = ['sqft', 'bedrooms', 'bathrooms', 'year_built']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough'
)

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

preds = model.predict(X_test)
preds = model.predict(X_test)

rmse = sqrt(mean_squared_error(y_test, preds))
mae = mean_absolute_error(y_test, preds)
r2 = r2_score(y_test, preds)

print("\nModel Evaluation")
print("-------------------------")
print(f"RMSE: ${rmse:,.2f}")
print(f"MAE : ${mae:,.2f}")
print(f"R²  : {r2:.4f}")

# Show actual price vs predicted price
results = pd.DataFrame({
    'Actual Price': y_test.values,
    'Predicted Price': preds
})

results['Difference'] = results['Actual Price'] - results['Predicted Price']

print("\nActual vs Predicted Prices:")
print(results.head(10).to_string(index=False))


os.makedirs('model', exist_ok=True)
joblib.dump(model, 'model/house_price_model.pkl')

with open('model/features.json', 'w') as f:
    json.dump(features, f)

print("Model saved to model/house_price_model.pkl")
print("Columns in CSV:", df.columns.tolist())
print("First few rows:\n", df.head())