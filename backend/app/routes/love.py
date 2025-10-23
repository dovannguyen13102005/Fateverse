from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict
from ..services.love import calculate_love_compatibility
from pydantic import BaseModel

router = APIRouter()

class LoveMatchRequest(BaseModel):
    name1: str
    birth_date1: datetime
    name2: str
    birth_date2: datetime

@router.post("/{user_id}")
async def get_love_compatibility(user_id: str, request: LoveMatchRequest) -> Dict:
    try:
        result = await calculate_love_compatibility(
            user_id=user_id,
            name1=request.name1,
            birth_date1=request.birth_date1,
            name2=request.name2,
            birth_date2=request.birth_date2
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))