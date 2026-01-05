import os
import pandas as pd
import numpy as np
import json
import xgboost as xgb
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from app.database import SQLALCHEMY_DATABASE_URL

# Ensure directory exists
os.makedirs('models', exist_ok=True)

# 1. Fetch data from PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
query = "SELECT * FROM predictions"
df = pd.read_sql(query, engine)

print(f"Training model using {len(df)} rows fetched from PostgreSQL.")
print(f"\n📊 Price Statistics (in original currency - INR):")
print(f"   Min: ₹{df['predicted_price'].min():,.0f}")
print(f"   Max: ₹{df['predicted_price'].max():,.0f}")
print(f"   Mean: ₹{df['predicted_price'].mean():,.0f}")
print(f"   Median: ₹{df['predicted_price'].median():,.0f}")

# 2. Preprocessing
binary_map = {'yes': 1, 'no': 0}
binary_cols = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
for col in binary_cols:
    df[col] = df[col].map(binary_map)

# One-Hot Encoding
df = pd.get_dummies(df, columns=['furnishingstatus'], prefix='furnish')

# 3. Features and Target Selection
X = df.drop(['id', 'created_at', 'predicted_price'], axis=1)
y = np.log1p(df['predicted_price'])  # Log transform
feature_names = list(X.columns)

print(f"\n📈 After log1p transform:")
print(f"   Min: {y.min():.4f}")
print(f"   Max: {y.max():.4f}")
print(f"   Mean: {y.mean():.4f}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train Model
model = xgb.XGBRegressor(
    n_estimators=1000, 
    learning_rate=0.05, 
    max_depth=5, 
    early_stopping_rounds=50,
    random_state=42
)

model.fit(
    X_train, y_train, 
    eval_set=[(X_test, y_test)], 
    verbose=False
)

# 5. Evaluate
y_pred_log = model.predict(X_test)
y_pred_actual = np.expm1(y_pred_log)
y_test_actual = np.expm1(y_test)

print(f"\n✅ Training Complete!")
print(f"   R2 Score: {r2_score(y_test, y_pred_log):.4f}")
print(f"   MAE: ₹{mean_absolute_error(y_test_actual, y_pred_actual):,.0f}")

print(f"\n🔍 Sample Predictions:")
for i in range(min(3, len(y_test_actual))):
    print(f"   Actual: ₹{y_test_actual.iloc[i]:,.0f} | Predicted: ₹{y_pred_actual[i]:,.0f}")

# 6. Save Artifacts
model.get_booster().save_model('models/house_model.json')

metadata = {
    "features": feature_names,
    "stats": {
        "area_max": int(df['area'].max()),
        "area_min": int(df['area'].min()),
        "price_min": float(df['predicted_price'].min()),
        "price_max": float(df['predicted_price'].max()),
        "price_mean": float(df['predicted_price'].mean())
    },
    "binary_mapping": binary_map,
    "expected_furnish_categories": ['furnished', 'semi-furnished', 'unfurnished'],
    "currency": "INR"
}

with open('models/model_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print("\n💾 Model and metadata saved successfully!")