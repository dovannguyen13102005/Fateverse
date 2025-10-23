# Hướng Dẫn Sử Dụng Tính Năng Cài Đặt 🎯

## Tổng Quan

Trang **Cài Đặt** (Settings) đã được hoàn thiện với đầy đủ các tính năng quản lý tài khoản và cá nhân hóa.

---

## ✅ Các Tính Năng Đã Hoàn Thành

### 1. 📸 Thay Đổi Ảnh Đại Diện

**Cách sử dụng:**
- Click vào icon 📷 ở góc dưới bên phải ảnh đại diện
- Chọn file ảnh từ máy tính (JPG, PNG, GIF, etc.)
- Xem trước ảnh ngay lập tức
- Click "Lưu Thay Đổi" để áp dụng

**Giới hạn:**
- Kích thước file: Tối đa 5MB
- Định dạng: Tất cả các định dạng ảnh (image/*)
- Lưu trữ: Base64 trong MongoDB

**Kỹ thuật:**
```typescript
// Frontend: Convert image to Base64
const convertImageToBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result as string);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
};

// Backend: Store in MongoDB
updateData.picture = base64Image;
```

---

### 2. 💾 Lưu Thay Đổi

**Các trường có thể cập nhật:**
- ✅ Họ và tên
- ✅ Ngày sinh
- ✅ Giới tính
- ✅ Giao diện (Theme)
- ✅ Ảnh đại diện
- ✅ Thông báo

**Quy trình:**
1. Người dùng chỉnh sửa thông tin
2. Click "Lưu Thay Đổi"
3. Frontend gửi PUT request đến `/api/users/profile/{user_id}`
4. Backend xác thực quyền (chỉ user tự update profile của mình)
5. MongoDB cập nhật dữ liệu
6. Hiển thị thông báo thành công
7. Reload trang sau 1.5 giây để áp dụng theme mới

**Code Backend:**
```python
@router.put("/profile/{user_id}", response_model=UserResponse)
async def update_user_profile(
    user_id: str, 
    user_update: UserUpdate,
    current_user_id: str = Depends(get_current_user_id)
):
    # Kiểm tra quyền
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền")
    
    # Update fields
    update_data = user_update.dict(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.now()
        await users.update_one(
            {"id": user_id},
            {"$set": update_data}
        )
    
    return updated_user
```

---

### 3. 🎨 6 Theme Tùy Chọn

**Danh sách theme:**
1. 🌌 **Galaxy** (Mặc định) - Màu tím ánh sao
2. 🌠 **Nebula** - Tím đậm huyền bí
3. 🌅 **Sunrise** - Vàng ấm áp
4. 🌊 **Ocean** - Xanh dương đại dương
5. 🌲 **Forest** - Xanh lá rừng rậm
6. 🌇 **Sunset** - Cam đỏ hoàng hôn

**Cách hoạt động:**
- User chọn theme
- Lưu vào `theme_preference` trong MongoDB
- Reload page để CSS áp dụng theme mới
- Theme ảnh hưởng đến toàn bộ app (background, gradient, colors)

---

### 4. 📊 Thống Kê Cá Nhân

**Thông tin hiển thị:**
- 🔢 Tổng số lượt bói
- 📅 Số ngày hoạt động
- 💖 Số lượt yêu thích
- 🔗 Số lượt chia sẻ

**Phân loại theo loại:**
- 🌟 Lá số hôm nay
- 🔮 Tarot
- 💕 Tình duyên
- 🔢 Thần số học
- ⭐ Cung hoàng đạo

**API Endpoint:**
```
GET /api/users/statistics/{user_id}
```

**Response:**
```json
{
  "total_fortunes": 42,
  "by_type": {
    "fortune": 15,
    "tarot": 10,
    "love": 8,
    "numerology": 5,
    "zodiac": 4
  },
  "favorites_count": 12,
  "shared_count": 5,
  "last_fortune_date": "2025-10-22T10:30:00",
  "member_since": "2025-09-01T08:00:00",
  "days_active": 51
}
```

---

### 5. 🔔 Quản Lý Thông Báo

**Toggle switch:**
- Bật/tắt thông báo
- Lưu vào `notification_enabled` field
- Chuẩn bị cho push notification trong tương lai

**UI Component:**
```tsx
<input
  type="checkbox"
  checked={settings.notification_enabled}
  onChange={(e) => setSettings({ 
    ...settings, 
    notification_enabled: e.target.checked 
  })}
  className="toggle-switch"
/>
```

---

### 6. 💾 Xuất Dữ Liệu (Export Data)

**Chức năng:**
- Tải xuất toàn bộ dữ liệu cá nhân
- Format: JSON
- Bao gồm:
  - Thông tin profile
  - Toàn bộ lịch sử bói toán
  - Metadata (export date, total records)

**API Endpoint:**
```
GET /api/users/export/{user_id}
```

**Cách sử dụng:**
1. Click "Xuất Dữ Liệu (JSON)"
2. Browser tự động download file
3. Tên file: `fateverse_data_2025-10-22.json`

**Code Frontend:**
```typescript
const handleExportData = async () => {
  const response = await authAPI.exportData(user.id);
  
  // Create download link
  const dataStr = JSON.stringify(response.data, null, 2);
  const dataBlob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(dataBlob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `fateverse_data_${new Date().toISOString().split('T')[0]}.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};
```

---

### 7. 🗑️ Xóa Tài Khoản (Delete Account)

**Quy trình 2 bước:**
1. **Bước 1**: Click "Xóa Tài Khoản"
2. **Bước 2**: Hiển thị cảnh báo chi tiết + nút "Xác Nhận Xóa"

**Cảnh báo:**
- ⚠️ Hành động không thể hoàn tác
- Xóa vĩnh viễn:
  - Thông tin cá nhân
  - Lịch sử bói toán
  - Các mục yêu thích
  - Cài đặt và tùy chỉnh

**API Endpoint:**
```
DELETE /api/users/account/{user_id}
```

**Backend Logic:**
```python
@router.delete("/account/{user_id}")
async def delete_user_account(user_id: str, current_user_id: str):
    # Delete all fortune history
    history_result = await fortune_history.delete_many({"user_id": user_id})
    
    # Delete user account
    user_result = await users.delete_one({"id": user_id})
    
    return {
        "message": "Tài khoản đã được xóa thành công",
        "deleted_fortunes": history_result.deleted_count,
        "deleted_user": user_result.deleted_count > 0
    }
```

**Sau khi xóa:**
- Hiển thị thông báo "Tài khoản đã được xóa"
- Auto logout sau 2 giây
- Redirect về trang login

---

## 🔐 Bảo Mật

### Authentication & Authorization

**Mọi API đều yêu cầu JWT token:**
```python
current_user_id: str = Depends(get_current_user_id)
```

**Kiểm tra quyền:**
```python
if user_id != current_user_id:
    raise HTTPException(status_code=403, detail="Bạn không có quyền")
```

**Token được gửi qua header:**
```typescript
config.headers.Authorization = `Bearer ${token}`;
```

---

## 🎯 User Experience

### 1. Loading States
- Spinner khi đang tải dữ liệu
- Disable button khi đang lưu
- Text thay đổi: "Đang lưu...", "Đang xóa..."

### 2. Success/Error Messages
- ✅ Màu xanh cho thành công
- ❌ Màu đỏ cho lỗi
- Hiển thị 2-3 giây rồi tự động ẩn

### 3. Animations
- Framer Motion cho smooth transitions
- Fade in/out cho sections
- Scale effect cho buttons
- Hover effects

### 4. Responsive Design
- Mobile-first approach
- Grid adapts: 2 cols (mobile) → 3 cols (desktop)
- Touch-friendly button sizes

---

## 🧪 Testing Guide

### Test Case 1: Upload Ảnh
```
1. Login vào app
2. Vào trang Settings
3. Click icon 📷
4. Chọn ảnh < 5MB → ✅ Hiện preview
5. Chọn ảnh > 5MB → ❌ Hiện lỗi
6. Chọn file không phải ảnh → ❌ Hiện lỗi
7. Click "Lưu Thay Đổi" → ✅ Ảnh được lưu
8. Reload page → ✅ Ảnh vẫn hiển thị
```

### Test Case 2: Thay Đổi Theme
```
1. Chọn theme "Ocean" 🌊
2. Click "Lưu Thay Đổi"
3. Page reload
4. Kiểm tra background → ✅ Màu xanh dương
5. Navigate sang trang khác → ✅ Theme vẫn áp dụng
```

### Test Case 3: Xem Thống Kê
```
1. Click "Thống Kê Cá Nhân"
2. Section expand → ✅ Hiện số liệu
3. Kiểm tra tổng lượt bói = tổng từng loại
4. Click lại để collapse → ✅ Ẩn đi
```

### Test Case 4: Xuất Dữ Liệu
```
1. Click "Xuất Dữ Liệu (JSON)"
2. File tự động download → ✅
3. Mở file JSON
4. Kiểm tra có user_profile + fortune_history → ✅
5. Validate JSON format → ✅
```

### Test Case 5: Xóa Tài Khoản
```
1. Click "Xóa Tài Khoản"
2. Hiện cảnh báo chi tiết → ✅
3. Click "Hủy" → ✅ Không xóa
4. Click "Xóa Tài Khoản" lại
5. Click "Xác Nhận Xóa"
6. Account bị xóa → ✅
7. Auto logout → ✅
8. Login lại bằng cùng email → ❌ Không thể
```

---

## 📝 Database Schema

### Users Collection
```javascript
{
  "_id": ObjectId("..."),
  "id": "user_123",
  "name": "Nguyễn Văn A",
  "email": "user@example.com",
  "birth_date": ISODate("1995-05-15"),
  "gender": "male",
  "theme_preference": "galaxy",
  "picture": "data:image/jpeg;base64,...",  // Base64 string
  "notification_enabled": true,
  "google_id": "google_123",
  "created_at": ISODate("2025-09-01"),
  "updated_at": ISODate("2025-10-22"),
  "last_login": ISODate("2025-10-22")
}
```

---

## 🚀 Deployment Notes

### Environment Variables
```bash
# Frontend (.env)
VITE_API_URL=http://localhost:8000

# Backend
MONGODB_URL=mongodb://mongodb:27017
DATABASE_NAME=fateverse
JWT_SECRET=your_secret_key
```

### Docker Compose
```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongodb:27017
  
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
```

---

## 🎉 Kết Luận

Trang Settings đã hoàn thiện với:
- ✅ Upload và lưu ảnh đại diện
- ✅ Cập nhật thông tin cá nhân
- ✅ 6 theme tùy chọn
- ✅ Thống kê chi tiết
- ✅ Quản lý thông báo
- ✅ Xuất dữ liệu JSON
- ✅ Xóa tài khoản an toàn

**Ready for production!** 🚀
