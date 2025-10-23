from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict, Optional
from ..services.tarot import get_tarot_reading
from pydantic import BaseModel

router = APIRouter()

class TarotRequest(BaseModel):
    spread_type: str = "past_present_future"
    num_cards: Optional[int] = None
    question: str = ""

@router.post("/{user_id}")
async def get_tarot(user_id: str, request: TarotRequest) -> Dict:
    """
    Xem bói tarot
    
    Các loại trải bài:
    - single_card: Rút 1 lá bài
    - past_present_future: Quá khứ - Hiện tại - Tương lai (3 lá)
    - celtic_cross: Thập giá Celtic (10 lá)
    """
    try:
        result = await get_tarot_reading(
            user_id=user_id,
            spread_type=request.spread_type,
            num_cards=request.num_cards,
            question=request.question
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))