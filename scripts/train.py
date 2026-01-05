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

# 2. Preprocessing
binary_map = {'yes': 1, 'no': 0}
binary_cols = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
for col in binary_cols:
    df[col] = df[col].map(binary_map)

# One-Hot Encoding
df = pd.get_dummies(df, columns=['furnishingstatus'], prefix='furnish')

# 3. Features and Target Selection
# IMPORTANT: We drop 'id' and 'created_at' because they are DB artifacts, not house features.
# We use 'predicted_price' because that is the column name in our Postgres table.
X = df.drop(['id', 'created_at', 'predicted_price'], axis=1)
y = np.log1p(df['predicted_price']) 
feature_names = list(X.columns)

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

# 5. Save Artifacts
model.get_booster().save_model('models/house_model.json')

metadata = {
    "features": feature_names,
    "stats": {
        "area_max": int(df['area'].max()),
        "area_min": int(df['area'].min())
    },
    "binary_mapping": binary_map,
    "expected_furnish_categories": ['furnished', 'semi-furnished', 'unfurnished']
}

with open('models/model_metadata.json', 'w') as f:
    json.dump(metadata, f)

print(f"✅ Training Complete.")
print(f"R2 Score: {r2_score(y_test, model.predict(X_test)):.4f}")
print("Metadata and model synced with Database schema.")