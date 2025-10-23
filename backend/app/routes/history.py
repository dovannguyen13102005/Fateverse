from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
from datetime import datetime
from bson import ObjectId
from ..database.mongodb import fortune_history
from .auth import get_current_user_id

router = APIRouter()

@router.get("/{user_id}")
async def get_user_history(user_id: str, limit: int = 50) -> List[Dict]:
    """Lấy lịch sử xem bói của người dùng"""
    try:
        cursor = fortune_history.find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(limit)
        
        history = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            doc["id"] = doc["_id"]
            history.append(doc)
        
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Không thể lấy lịch sử: {str(e)}")

@router.get("/type/{user_id}/{fortune_type}")
async def get_history_by_type(user_id: str, fortune_type: str, limit: int = 20) -> List[Dict]:
    """Lấy lịch sử theo loại (numerology, zodiac, tarot, etc.)"""
    try:
        cursor = fortune_history.find(
            {"user_id": user_id, "type": fortune_type}
        ).sort("created_at", -1).limit(limit)
        
        history = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            doc["id"] = doc["_id"]
            history.append(doc)
        
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Không thể lấy lịch sử: {str(e)}")

@router.delete("/{history_id}")
async def delete_history(history_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Xóa một mục trong lịch sử"""
    try:
        # Kiểm tra xem history có thuộc về user không
        history_item = await fortune_history.find_one({"_id": ObjectId(history_id)})
        
        if not history_item:
            raise HTTPException(status_code=404, detail="Không tìm thấy lịch sử")
        
        if history_item["user_id"] != current_user_id:
            raise HTTPException(status_code=403, detail="Bạn không có quyền xóa lịch sử này")
        
        result = await fortune_history.delete_one({"_id": ObjectId(history_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Không thể xóa lịch sử")
        
        return {"message": "Đã xóa lịch sử thành công", "id": history_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi xóa lịch sử: {str(e)}")

@router.delete("/user/{user_id}/all")
async def delete_all_history(user_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Xóa toàn bộ lịch sử của người dùng"""
    try:
        if user_id != current_user_id:
            raise HTTPException(status_code=403, detail="Bạn không có quyền xóa lịch sử này")
        
        result = await fortune_history.delete_many({"user_id": user_id})
        
        return {
            "message": f"Đã xóa {result.deleted_count} mục lịch sử",
            "deleted_count": result.deleted_count
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi xóa lịch sử: {str(e)}")

@router.post("/{history_id}/favorite")
async def toggle_favorite(history_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Đánh dấu/Bỏ đánh dấu yêu thích"""
    try:
        history_item = await fortune_history.find_one({"_id": ObjectId(history_id)})
        
        if not history_item:
            raise HTTPException(status_code=404, detail="Không tìm thấy lịch sử")
        
        if history_item["user_id"] != current_user_id:
            raise HTTPException(status_code=403, detail="Bạn không có quyền thao tác lịch sử này")
        
        # Toggle favorite status
        is_favorite = history_item.get("is_favorite", False)
        new_favorite_status = not is_favorite
        
        await fortune_history.update_one(
            {"_id": ObjectId(history_id)},
            {"$set": {"is_favorite": new_favorite_status, "updated_at": datetime.now()}}
        )
        
        return {
            "message": "Đã cập nhật trạng thái yêu thích",
            "is_favorite": new_favorite_status
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi cập nhật yêu thích: {str(e)}")

@router.get("/{user_id}/favorites")
async def get_favorites(user_id: str, limit: int = 50) -> List[Dict]:
    """Lấy danh sách các mục yêu thích"""
    try:
        cursor = fortune_history.find(
            {"user_id": user_id, "is_favorite": True}
        ).sort("created_at", -1).limit(limit)
        
        favorites = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            doc["id"] = doc["_id"]
            favorites.append(doc)
        
        return favorites
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Không thể lấy danh sách yêu thích: {str(e)}")

@router.post("/{history_id}/share")
async def create_share_link(history_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Tạo link chia sẻ công khai"""
    try:
        history_item = await fortune_history.find_one({"_id": ObjectId(history_id)})
        
        if not history_item:
            raise HTTPException(status_code=404, detail="Không tìm thấy lịch sử")
        
        if history_item["user_id"] != current_user_id:
            raise HTTPException(status_code=403, detail="Bạn không có quyền chia sẻ lịch sử này")
        
        # Tạo share token
        share_token = str(ObjectId())
        
        await fortune_history.update_one(
            {"_id": ObjectId(history_id)},
            {
                "$set": {
                    "share_token": share_token,
                    "is_shared": True,
                    "shared_at": datetime.now()
                }
            }
        )
        
        return {
            "message": "Đã tạo link chia sẻ",
            "share_token": share_token,
            "share_url": f"/share/{share_token}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi tạo link chia sẻ: {str(e)}")

@router.get("/share/{share_token}")
async def get_shared_fortune(share_token: str):
    """Xem kết quả được chia sẻ"""
    try:
        history_item = await fortune_history.find_one(
            {"share_token": share_token, "is_shared": True}
        )
        
        if not history_item:
            raise HTTPException(status_code=404, detail="Không tìm thấy kết quả chia sẻ")
        
        history_item["_id"] = str(history_item["_id"])
        history_item["id"] = history_item["_id"]
        
        # Không trả về user_id để bảo mật
        history_item.pop("user_id", None)
        
        return history_item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lấy kết quả chia sẻ: {str(e)}")

@router.delete("/{history_id}/share")
async def remove_share_link(history_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Xóa link chia sẻ"""
    try:
        history_item = await fortune_history.find_one({"_id": ObjectId(history_id)})
        
        if not history_item:
            raise HTTPException(status_code=404, detail="Không tìm thấy lịch sử")
        
        if history_item["user_id"] != current_user_id:
            raise HTTPException(status_code=403, detail="Bạn không có quyền thao tác lịch sử này")
        
        await fortune_history.update_one(
            {"_id": ObjectId(history_id)},
            {
                "$set": {"is_shared": False},
                "$unset": {"share_token": "", "shared_at": ""}
            }
        )
        
        return {"message": "Đã xóa link chia sẻ"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi xóa link chia sẻ: {str(e)}")
