from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict
from ..services.zodiac import calculate_zodiac
from pydantic import BaseModel

router = APIRouter()

class ZodiacRequest(BaseModel):
    birth_date: datetime

@router.post("/{user_id}")
async def get_zodiac(user_id: str, request: ZodiacRequest) -> Dict:
    try:
        result = await calculate_zodiac(
            user_id=user_id,
            birth_date=request.birth_date
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))