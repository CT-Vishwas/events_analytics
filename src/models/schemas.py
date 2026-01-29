from pydantic import BaseModel, field_validator, ValidationError, Field, EmailStr
from datetime import datetime
from ..utils.logger import get_logger

logger = get_logger(__name__)

class EventSchema(BaseModel):
    event_id: str
    topic: str
    city: str
    venue_capacity: int = Field(gt=0, description="venue capacity must be greater than 0")
    scheduled_date_time: datetime

    instructor_id:str

class AttendeeSchema(BaseModel):
    attendee_email: EmailStr
    industry: str
    company: str

    @field_validator('industry')
    @classmethod
    def validate_industry(cls, v):
        allowed = ["IT", "Finance", "Education", "Manufacturing", "Healthcare"]
        if v not in allowed:
            logger.warning(f"Validation Warning: Non-standard industry detected: {v}")
        return v

class RegistrationSchema(BaseModel):
    registration_id: str
    event_id: str
    attendee_email: EmailStr
    registration_date: datetime
    payment_status: str

    @field_validator('payment_status')
    @classmethod
    def validate_payment_status(cls, v):
        allowed = ["Pending", "Completed", "Failed"]
        if v not in allowed:
            logger.warning(f"Validation Warning: Non-standard payment status detected: {v}")
        return v
    
class PricingSchema(BaseModel):
    event_id: str
    ticket_type: str
    price: float = Field(gt=0, description="Price must be greater than 0")
    currency: str

    @field_validator('currency')
    @classmethod
    def validate_currency(cls, v):
        allowed = ["USD", "EUR", "INR", "GBP"]
        if v not in allowed:
            logger.warning(f"Validation Warning: Non-standard currency detected: {v}")
        return v

class ChannelSchema(BaseModel):
    channel_id: str
    channel_name: str
    channel_type: str

    @field_validator('channel_type')
    @classmethod
    def validate_channel_type(cls, v):
        allowed = ["Online", "Offline", "Hybrid"]
        if v not in allowed:
            logger.warning(f"Validation Warning: Non-standard channel type detected: {v}")
        return v