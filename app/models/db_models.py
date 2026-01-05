from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime, timezone
from ..database import Base
class PredictionRecord(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    area = Column(Integer)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    stories = Column(Integer)
    mainroad = Column(String)
    guestroom = Column(String)
    basement = Column(String)
    hotwaterheating = Column(String)
    airconditioning = Column(String)
    parking = Column(Integer)
    prefarea = Column(String)
    furnishingstatus = Column(String)
    
    predicted_price = Column(Float)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

