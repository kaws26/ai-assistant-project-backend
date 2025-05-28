from pydantic import BaseModel
from datetime import datetime

class GenerateRequest(BaseModel):
    user_id: str
    query: str

class GenerateResponse(BaseModel):
    casual_response: str
    formal_response: str

class HistoryItem(BaseModel):
    id: str
    query: str
    casual_response: str
    formal_response: str
    created_at: datetime

class HistoryResponse(BaseModel):
    history: list[HistoryItem]