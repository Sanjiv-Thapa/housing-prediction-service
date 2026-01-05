import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from app.database import SQLALCHEMY_DATABASE_URL

def clear_data():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    # Delete all records from predictions table
    with engine.connect() as conn:
        result = conn.execute("DELETE FROM predictions")
        conn.commit()
        print(f"✅ Deleted all records from predictions table")

if __name__ == "__main__":
    clear_data()