from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone
from typing import List

class Review(BaseModel):
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    rating: float
    reason: str

class Employee(BaseModel):
    discord_id: str
    name: str
    role: str
    email: EmailStr
    stars: float = 5.0
    status: str = "Ativo"
    reviews: List[Review] = []