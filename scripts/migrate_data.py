import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os 
from app.database import SQLALCHEMY_DATABASE_URL
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from app.models.db_models import PredictionRecord

def migrate():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    if not os.path.exists('data/raw/housing.csv'):


        print("Error:Housing.csv not found in root directory")
        return
    df = pd.read_csv('data/raw/housing.csv')
    print(f" loaded{len(df)} rows from csv")
    df_to_db = df.rename(columns={'price':'predicted_price'})

    try:
        df_to_db.to_sql('predictions',engine, if_exists='append', index=False)
        print("Data migration completed successfully.")
    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == "__main__":
    migrate()


    

