from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AlertBase(BaseModel):
    message: str
    user_email: str

class AlertCreate(AlertBase):
    pass

class AlertOut(AlertBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True