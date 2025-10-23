from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from typing import Dict
from ..models.user import UserBase, UserCreate, UserInDB, UserResponse, UserUpdate
from ..services.numerology import calculate_numerology
from ..database.mongodb import users
from ..routes.auth import get_current_user_id
from bson import ObjectId

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    # Kiểm tra email đã tồn tại
    if await users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email này đã được đăng ký")
    
    # Tạo document người dùng
    user_dict = user.dict()
    user_dict["created_at"] = datetime.now()
    user_dict["id"] = str(ObjectId())
    
    # Thêm vào database
    await users.insert_one(user_dict)
    
    return UserResponse(**user_dict)

@router.get("/profile/{user_id}", response_model=UserResponse)
async def get_user_profile(user_id: str):
    user = await users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    return UserResponse(**user)

@router.put("/profile/{user_id}", response_model=UserResponse)
async def update_user_profile(
    user_id: str, 
    user_update: UserUpdate,
    current_user_id: str = Depends(get_current_user_id)
):
    """Update user profile"""
    # Check if user is updating their own profile
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền cập nhật hồ sơ này")
    
    # Get existing user
    existing_user = await users.find_one({"id": user_id})
    if not existing_user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    
    # Update fields
    update_data = user_update.dict(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.now()
        await users.update_one(
            {"id": user_id},
            {"$set": update_data}
        )
    
    # Get updated user
    updated_user = await users.find_one({"id": user_id})
    return UserResponse(**updated_user)

@router.post("/numerology/{user_id}")
async def calculate_user_numerology(user_id: str) -> Dict:
    user = await users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = await calculate_numerology(
        user_id=user_id,
        name=user["name"],
        birth_date=user["birth_date"]
    )
    
    return result

@router.get("/statistics/{user_id}")
async def get_user_statistics(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """Get user statistics"""
    from ..database.mongodb import fortune_history
    
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền xem thống kê này")
    
    user = await users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    
    # Count total fortunes
    total_fortunes = await fortune_history.count_documents({"user_id": user_id})
    
    # Count by type
    fortune_types = ["fortune", "tarot", "love", "numerology", "zodiac"]
    type_counts = {}
    for fortune_type in fortune_types:
        count = await fortune_history.count_documents({
            "user_id": user_id,
            "type": fortune_type
        })
        type_counts[fortune_type] = count
    
    # Count favorites
    favorites_count = await fortune_history.count_documents({
        "user_id": user_id,
        "is_favorite": True
    })
    
    # Count shared
    shared_count = await fortune_history.count_documents({
        "user_id": user_id,
        "is_shared": True
    })
    
    # Get most recent fortune
    recent_fortune = await fortune_history.find_one(
        {"user_id": user_id},
        sort=[("created_at", -1)]
    )
    
    return {
        "total_fortunes": total_fortunes,
        "by_type": type_counts,
        "favorites_count": favorites_count,
        "shared_count": shared_count,
        "last_fortune_date": recent_fortune["created_at"] if recent_fortune else None,
        "member_since": user.get("created_at"),
        "days_active": (datetime.now() - user.get("created_at", datetime.now())).days
    }

@router.delete("/account/{user_id}")
async def delete_user_account(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """Delete user account and all associated data"""
    from ..database.mongodb import fortune_history
    
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền xóa tài khoản này")
    
    user = await users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    
    # Delete all fortune history
    history_result = await fortune_history.delete_many({"user_id": user_id})
    
    # Delete user account
    user_result = await users.delete_one({"id": user_id})
    
    return {
        "message": "Tài khoản đã được xóa thành công",
        "deleted_fortunes": history_result.deleted_count,
        "deleted_user": user_result.deleted_count > 0
    }

@router.get("/export/{user_id}")
async def export_user_data(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """Export all user data"""
    from ..database.mongodb import fortune_history
    
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền xuất dữ liệu này")
    
    user = await users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    
    # Get all fortune history
    cursor = fortune_history.find({"user_id": user_id})
    history = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        history.append(doc)
    
    # Remove internal MongoDB _id from user
    user["_id"] = str(user["_id"]) if "_id" in user else None
    
    return {
        "user_profile": user,
        "fortune_history": history,
        "export_date": datetime.now().isoformat(),
        "total_records": len(history)
    }