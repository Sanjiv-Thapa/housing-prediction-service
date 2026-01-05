from fastapi import APIRouter, HTTPException,Depends
from ...schemas.houses import HousePredictionInputSchema, HousePricePredictionOutputSchema
from ...services.model_service import model_services
from sqlalchemy.orm import Session
from ...database import get_db
from ...models.db_models import PredictionRecord

router = APIRouter()

@router.post("/")
def predict_price(payload: HousePredictionInputSchema, db: Session = Depends(get_db)):
    try:
        # 1. Get Prediction from ML Service
        prediction = model_services.predict(payload)
        
        # 2. Save to PostgreSQL
        db_record = PredictionRecord(
            **payload.model_dump(),
            predicted_price=prediction
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        
        return {
            "predicted_price": prediction,
            "record_id": db_record.id,
            "status": "Saved to Database"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
