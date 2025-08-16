from pydantic import BaseModel, Field
from typing import Optional, List


class Invoice(BaseModel):
    date: Optional[str] = Field(None, alias="Date")
    sum: Optional[float] = Field(None, alias="Sum")
    correspondent: Optional[str] = Field(None, alias="Correspondent")
    bank: Optional[str] = Field(None, alias="Bank")
    payment_destination: Optional[str] = Field(None, alias="Payment Destination")
    transfer_type: Optional[str] = Field(None, alias="Transfer Type")

    class Config:
        populate_by_name = True


class InvoiceList(BaseModel):
    invoices: List[Invoice] = Field(default_factory=list)
