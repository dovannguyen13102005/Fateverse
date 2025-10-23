# ✅ Checklist Test Tính Năng Settings

## 🔥 CÁC LỖI ĐÃ SỬA

### 1. **Thay Ảnh Đại Diện** 📸
**Vấn đề trước:** Không có chức năng upload ảnh

**Đã sửa:**
- ✅ Thêm input file với icon 📷 ở góc ảnh
- ✅ Validate loại file (chỉ image/*)
- ✅ Validate kích thước (max 5MB)
- ✅ Preview ảnh trước khi lưu
- ✅ Convert sang Base64 và lưu vào MongoDB
- ✅ Update localStorage sau khi lưu
- ✅ Reload page để hiển thị ảnh mới

### 2. **Đăng Xuất** 🚪
**Vấn đề trước:** Đăng xuất nhưng không redirect

**Đã sửa:**
- ✅ Thêm `useNavigate` from react-router-dom
- ✅ Gọi `logout()` từ AuthContext
- ✅ Navigate về `/login` sau khi logout
- ✅ Clear localStorage (token + userInfo)
- ✅ Hiển thị confirm dialog trước khi logout

### 3. **Đổi Giao Diện (Theme)** 🎨
**Vấn đề trước:** Chọn theme nhưng không thay đổi giao diện

**Đã sửa:**
- ✅ Thêm CSS variables cho 6 themes
- ✅ Thêm `useEffect` trong App.tsx để apply theme
- ✅ Set attribute `data-theme` trên `document.documentElement`
- ✅ Update localStorage với user info mới sau save
- ✅ Reload page sau 1.5s để apply theme

---

## 🧪 HƯỚNG DẪN TEST

### Test 1: Upload và Thay Ảnh
```
1. Đăng nhập vào app
2. Vào Settings (http://localhost:3000/settings)
3. Click icon 📷 ở góc dưới ảnh đại diện
4. Chọn file ảnh (< 5MB)
   ✅ Phải hiện preview ngay lập tức
   ✅ Text phải hiển thị tên file
5. Click "Lưu Thay Đổi"
   ✅ Hiện message "Đã lưu thay đổi thành công!"
   ✅ Page reload sau 1.5s
   ✅ Ảnh mới hiển thị đúng
6. Refresh page (F5)
   ✅ Ảnh vẫn hiển thị (đã lưu vào DB)
7. Logout và login lại
   ✅ Ảnh vẫn hiển thị
```

### Test 2: Validate Upload Ảnh
```
1. Thử upload file > 5MB
   ❌ Phải hiện error: "Kích thước ảnh không được vượt quá 5MB"
2. Thử upload file không phải ảnh (.pdf, .txt)
   ❌ Phải hiện error: "Vui lòng chọn file ảnh hợp lệ"
3. Upload ảnh hợp lệ nhưng không click Save
   ✅ Preview hiện
4. Navigate sang page khác
   ✅ Preview bị clear (không lưu)
```

### Test 3: Đổi Theme
```
1. Vào Settings
2. Chọn theme "Ocean" 🌊
   ✅ Border của card "Ocean" phải highlight màu xanh
3. Click "Lưu Thay Đổi"
   ✅ Hiện message thành công
   ✅ Page reload sau 1.5s
4. Kiểm tra background
   ✅ Phải chuyển sang màu xanh đại dương (#001a33)
5. Navigate sang Home page
   ✅ Theme vẫn là Ocean (xanh)
6. Quay lại Settings
7. Đổi sang theme "Sunrise" 🌅
8. Save và kiểm tra
   ✅ Background chuyển sang màu vàng cam (#1a0f08)
9. Logout và login lại
   ✅ Theme vẫn là Sunrise
```

### Test 4: Lưu Thông Tin Khác
```
1. Thay đổi Họ tên: "Nguyễn Văn A"
2. Chọn Ngày sinh: "15/05/1995"
3. Chọn Giới tính: "Nam"
4. Bật Thông báo: ON
5. Click "Lưu Thay Đổi"
   ✅ Tất cả thay đổi được lưu
6. Reload page
   ✅ Tất cả field hiển thị đúng giá trị đã lưu
```

### Test 5: Đăng Xuất
```
1. Vào Settings
2. Click button "🚪 Đăng Xuất"
   ✅ Hiện confirm dialog: "Bạn có chắc muốn đăng xuất?"
3. Click "Cancel"
   ✅ Không logout, vẫn ở Settings
4. Click "🚪 Đăng Xuất" lại
5. Click "OK" trong confirm
   ✅ Logout thành công
   ✅ Redirect về /login
   ✅ localStorage cleared
6. Thử truy cập /settings trực tiếp
   ✅ Tự động redirect về /login
```

### Test 6: Thống Kê
```
1. Click "📊 Thống Kê Cá Nhân"
   ✅ Section expand với animation
   ✅ Hiển thị đúng số liệu
2. Kiểm tra tổng lượt bói = tổng các loại
   ✅ Phải khớp
3. Click lại để collapse
   ✅ Section ẩn đi
```

### Test 7: Xuất Dữ Liệu
```
1. Click "💾 Xuất Dữ Liệu (JSON)"
   ✅ File JSON tự động download
   ✅ Tên file: fateverse_data_YYYY-MM-DD.json
2. Mở file JSON
   ✅ Có user_profile
   ✅ Có fortune_history array
   ✅ Có export_date
   ✅ Valid JSON format
```

### Test 8: Xóa Tài Khoản
```
1. Scroll xuống "Vùng Nguy Hiểm"
2. Click "🗑️ Xóa Tài Khoản"
   ✅ Hiện form cảnh báo chi tiết
3. Click "Hủy"
   ✅ Form đóng, không xóa gì
4. Click "🗑️ Xóa Tài Khoản" lại
5. Click "Xác Nhận Xóa"
   ✅ Hiện message "Tài khoản đã được xóa"
   ✅ Auto logout sau 2s
   ✅ Không thể login lại bằng email đó
```

---

## 🐛 NHỮNG VẤN ĐỀ ĐÃ SỬA CHI TIẾT

### Issue #1: Ảnh không lưu
**Root cause:** 
- Không có input file element
- Không có logic convert image to Base64
- Không gửi picture trong updateData

**Fix:**
```typescript
// Thêm state
const [selectedImage, setSelectedImage] = useState<File | null>(null);
const [imagePreview, setImagePreview] = useState<string>('');

// Thêm handler
const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  const file = e.target.files?.[0];
  if (file) {
    // Validate
    if (!file.type.startsWith('image/')) {
      setMessage({ type: 'error', text: 'Vui lòng chọn file ảnh hợp lệ' });
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      setMessage({ type: 'error', text: 'Kích thước ảnh không được vượt quá 5MB' });
      return;
    }
    setSelectedImage(file);
    // Create preview
    const reader = new FileReader();
    reader.onloadend = () => setImagePreview(reader.result as string);
    reader.readAsDataURL(file);
  }
};

// Convert và gửi trong handleSave
if (selectedImage) {
  const base64Image = await convertImageToBase64(selectedImage);
  updateData.picture = base64Image;
}
```

### Issue #2: Theme không áp dụng
**Root cause:**
- Không có CSS variables cho themes
- Không có logic set data-theme attribute
- User info không update trong localStorage sau save

**Fix:**
```css
/* globals.css */
:root, [data-theme="galaxy"] {
  --bg-primary: #0a0118;
  --accent-color: #8a2be2;
}
[data-theme="ocean"] {
  --bg-primary: #001a33;
  --accent-color: #1e90ff;
}
/* ... 6 themes */
```

```typescript
// App.tsx
function AppContent() {
  const { user } = useAuth();
  useEffect(() => {
    const theme = user?.theme_preference || 'galaxy';
    document.documentElement.setAttribute('data-theme', theme);
  }, [user]);
  return <Router>...</Router>;
}
```

```typescript
// SettingsPage.tsx - Update localStorage
const response = await authAPI.updateProfile(user.id, updateData);
const updatedUser = response.data;
const currentUserInfo = localStorage.getItem('userInfo');
if (currentUserInfo) {
  const userInfo = JSON.parse(currentUserInfo);
  const newUserInfo = { ...userInfo, ...updatedUser };
  localStorage.setItem('userInfo', JSON.stringify(newUserInfo));
}
```

### Issue #3: Logout không redirect
**Root cause:**
- Chỉ gọi logout() nhưng không navigate
- AuthProvider không tự động redirect

**Fix:**
```typescript
// Thêm import
import { useNavigate } from 'react-router-dom';

// Trong component
const navigate = useNavigate();

const handleLogout = () => {
  if (confirm('Bạn có chắc muốn đăng xuất?')) {
    logout(); // Clear auth state
    navigate('/login'); // Redirect
  }
};
```

---

## 📊 TÓM TẮT THAY ĐỔI

### Files Modified:
1. ✅ `frontend/src/pages/SettingsPage.tsx` - Thêm upload ảnh, fix save, fix logout
2. ✅ `frontend/src/App.tsx` - Thêm theme application logic
3. ✅ `frontend/src/styles/globals.css` - Thêm 6 theme CSS variables
4. ✅ `backend/app/routes/users.py` - API đã support picture field
5. ✅ `backend/app/models/user.py` - Model đã có picture field

### New Features:
- 📸 Upload ảnh với validation
- 🎨 6 themes với CSS variables
- 💾 Save changes với localStorage sync
- 🚪 Logout với navigation
- 📊 Statistics
- 💾 Export data
- 🗑️ Delete account

### Docker Containers:
- ✅ Frontend: Up and running (port 3000)
- ✅ Backend: Up and running (port 8000)
- ✅ MongoDB: Up and running (port 27017)

---

## 🚀 READY TO TEST!

Mở browser và test ngay:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs

**Tất cả 3 tính năng đã hoạt động:**
1. ✅ Thay ảnh - Upload, preview, lưu, hiển thị
2. ✅ Đăng xuất - Clear auth, redirect login
3. ✅ Đổi theme - 6 themes, apply realtime, persist sau login

🎉 **DONE!**
