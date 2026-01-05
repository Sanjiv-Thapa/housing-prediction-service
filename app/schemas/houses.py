from pydantic import BaseModel, Field,field_validator
from enum import Enum

# define an enumeration for categorical fields to prevent typos
class BinaryField(str,Enum):
    yes="yes"
    no="no"

#input schemas for user input to the api 
class HousePredictionInputSchema(BaseModel):
    area: int = Field(..., gt=100, lt=50000, example=7420)
    bedrooms: int = Field(..., ge=1, le=10, example=4)
    bathrooms: int = Field(..., ge=1, le=5, example=2)
    stories: int = Field(..., ge=1, le=4, example=3)
    mainroad: BinaryField = Field(...,example="yes"),
    guestroom: BinaryField = Field(...,example="no"), 
    basement: BinaryField = Field(...,example="yes"),
    hotwaterheating: BinaryField = Field(...,example="no"),
    airconditioning:BinaryField = Field(...,example="yes"),
    parking: int = Field(..., example=2, ge=0),
    prefarea: BinaryField = Field(...,example="yes"),
    furnishingstatus: str = Field(..., example="furnished")

    @field_validator('bathrooms')
    @classmethod
    def check_bath_not_exceed_beds(cls, v: int, info):
        # Access other fields using info.data
        if 'bedrooms' in info.data and v > info.data['bedrooms'] + 1:
            raise ValueError('Too many bathrooms for the number of bedrooms')
        return v


class HousePricePredictionOutputSchema(BaseModel):
    predicted_price: float = Field(..., description="Predicted price of the house")
    currency: str = "USD"