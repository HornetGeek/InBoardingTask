from pydantic import BaseModel,Field
from datetime import date, time
from typing import Optional, Dict, Any
from datetime import datetime

class BookingRequest(BaseModel):
    customer_id: int = Field(..., description="Customer ID")
    service_id: int = Field(..., description="Service ID")
    date: str = Field(..., description="Booking date in YYYY-MM-DD format")
    time: str = Field(..., description="Booking time in HH:MM format")
    additional_info: Optional[str] = Field(None, description="Additional booking information")
    
    # New optional fields
    order_id: Optional[int] = Field(None, description="Order ID")
    invoice_id: Optional[int] = Field(None, description="Invoice ID")
    cal_booking_id: Optional[str] = Field(None, description="Cal Booking ID")
    status: Optional[str] = Field(default="pending", description="Booking status")
        

class BookingResponse(BaseModel):
    message: str
    order_id: int
    invoice_id: int
    cal_booking_id: str
    status: str

class BookingDetails(BaseModel):
    id: Optional[int] = None
    customer_id: int = Field(default=0)
    service_id: int = Field(default=0)
    date: str = Field(default='')
    time: str = Field(default='')
    order_id: str = Field(default='')
    invoice_id: str = Field(default='')
    cal_booking_id: Optional[str] = None
    status: str = Field(default='pending')
    additional_info: Optional[str] = None