from pydantic import BaseModel, Field, field_validator

class AccountModel(BaseModel):
    Food: float= Field(..., description="")
    Meal: float = Field(..., description="")
    Cash: str = Field(..., description="")

    @field_validator('Food', 'Meal', 'Cash')
    def field_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError('Field must be positive.')
        return value