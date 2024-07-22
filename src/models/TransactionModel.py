from pydantic import BaseModel, Field, field_validator

class TransactionModel(BaseModel):
    Account_id: str = Field(..., description="the account id fild to identify")
    TotalAmount: float = Field(..., description="the total amount of the transaction.")
    Mcc: str = Field(..., description="the merchant category code.")
    Merchant: str = Field(..., description="the name of the merchant.")

    @field_validator('TotalAmount')
    def total_amount_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError('Total amount must be positive.')
        return value
    
    @field_validator('Account_id', 'Mcc', 'Merchant')
    def must_not_be_empty(cls, value):
        if not value or value.strip() == "":
            raise ValueError('Field must not be empty.')
        return value
