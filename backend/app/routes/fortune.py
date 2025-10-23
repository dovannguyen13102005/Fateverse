from fastapi import APIRouter, HTTPException
from typing import Dict
from ..services.fortune import get_daily_fortune

router = APIRouter()

@router.get("/{user_id}")
async def get_fortune(user_id: str) -> Dict:
    try:
        result = await get_daily_fortune(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))