from pydantic import BaseModel
from typing import Optional

class KeywordBase(BaseModel):
    word: str

class KeywordCreate(KeywordBase):
    pass

class KeywordOut(KeywordBase):
    id: int
    owner_id: int
    
    class Config:
        from_attributes = True

class KeywordWithOwner(KeywordOut):
    owner_email: str