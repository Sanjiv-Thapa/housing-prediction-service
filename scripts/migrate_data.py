import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from app.database import SQLALCHEMY_DATABASE_URL
from app.models.db_models import PredictionRecord

def migrate():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    # Check both possible CSV filenames
    csv_path = None
    if os.path.exists('data/raw/Housing.csv'):
        csv_path = 'data/raw/Housing.csv'
    elif os.path.exists('data/raw/housing.csv'):
        csv_path = 'data/raw/housing.csv'
    else:
        print("Error: Housing.csv not found in data/raw/")
        return
    
    # Read CSV
    df = pd.read_csv(csv_path)
    print(f"📁 Loaded {len(df)} rows from {csv_path}")
    print(f"📊 Price range: ₹{df['price'].min():,.0f} to ₹{df['price'].max():,.0f}")
    
    # Rename 'price' column to 'predicted_price' to match DB schema
    df_to_db = df.rename(columns={'price': 'predicted_price'})
    
    # Verify data before inserting
    print(f"📊 After rename - predicted_price range: ₹{df_to_db['predicted_price'].min():,.0f} to ₹{df_to_db['predicted_price'].max():,.0f}")
    
    # Insert into database
    try:
        df_to_db.to_sql('predictions', engine, if_exists='append', index=False)
        print("✅ Data migration completed successfully.")
    except Exception as e:
        print(f"❌ Error during migration: {e}")

if __name__ == "__main__":
    migrate()