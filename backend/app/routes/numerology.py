from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict
from ..services.numerology import calculate_numerology
from pydantic import BaseModel

router = APIRouter()

class NumerologyRequest(BaseModel):
    name: str
    birth_date: datetime

@router.post("/{user_id}")
async def get_numerology(user_id: str, request: NumerologyRequest) -> Dict:
    try:
        result = await calculate_numerology(
            user_id=user_id,
            name=request.name,
            birth_date=request.birth_date
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))