from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Optional

class FortuneHistoryBase(BaseModel):
    user_id: str
    type: str  # "tarot", "love", "zodiac", "numerology", "daily"
    result_summary: str
    result_detail: Dict
    created_at: datetime = datetime.now()

class FortuneHistoryCreate(FortuneHistoryBase):
    pass

class FortuneHistoryInDB(FortuneHistoryBase):
    id: str

    class Config:
        orm_mode = True

class TarotCard(BaseModel):
    card_id: str
    name: str
    meaning: str
    image_url: str
    category: str  # "love" or "work"

class LoveMatch(BaseModel):
    match_id: str
    user_id: str
    partner_name: str
    partner_birth_date: datetime
    compatibility_score: float
    analysis_text: str

class ZodiacData(BaseModel):
    zodiac_id: str
    name: str
    element: str
    description: str
    lucky_number: str
    lucky_color: str
    compatible_signs: list[str]

class NumerologyResult(BaseModel):
    numerology_id: str
    user_id: str
    life_path_number: int
    expression_number: int
    soul_urge_number: int
    personality_number: int
    analysis_text: str

class DailyFortune(BaseModel):
    fortune_date: datetime
    message: str
    lucky_color: str
    emoji: str
    quote: str