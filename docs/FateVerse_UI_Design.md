# 🎨 FateVerse – UI Design Specification (Đặc tả Giao Diện Người Dùng)

---

## 🌌 1. Tổng quan thiết kế

### 🎯 Mục tiêu
- Tạo trải nghiệm **thần bí nhưng hiện đại**, pha vibe “AI cosmic” và “chiêm tinh”.
- Ưu tiên **UI thân thiện, cảm xúc và dễ share**.
- Dễ mở rộng, dùng lại component cho nhiều loại bói khác nhau.

### 💎 Concept chủ đạo
- **Tone màu:**  
  - Nền: `#0f0c29 → #302b63 → #24243e` (gradient vũ trụ)  
  - Accent: `#E0B0FF`, `#FFD700`, `#8A2BE2`
- **Font:** `Quicksand`, `Cinzel Decorative`
- **Icon set:** `Lucide Icons` hoặc `Heroicons`
- **Hiệu ứng:** Particle background, Glow animation, Framer Motion transition.

---

## 🏠 2. Giao diện tổng thể

| Màn hình | Mục đích | Thành phần chính |
|-----------|-----------|------------------|
| Home Page | Chọn loại bói | Header, Card menu (5 loại bói), CTA |
| Numerology Page | Tính thần số học | Form nhập tên + ngày sinh, kết quả |
| Zodiac Page | Cung hoàng đạo | Input ngày sinh, auto hiển thị cung |
| LoveMatch Page | Hợp đôi | Hai input, nút bói, kết quả % + lời khuyên |
| Tarot Page | Bói tarot | Deck bài, animation lật, kết quả 3 lá |
| Daily Fortune Page | Lá số hôm nay | Fortune card, quote + emoji |
| History Page | Lịch sử | Danh sách card, nút share/xóa |
| Settings Page | Cá nhân hóa | Theme, thông tin, logout |

---

## 🧩 3. Thành phần UI chi tiết

### 🧿 Header / Navigation
- Logo: “FateVerse 🔮”
- Items: Home / Numerology / Zodiac / Love / Tarot / Daily / History / Settings
- Mobile: collapsible sidebar.

---

### 🧮 Numerology Page
**Layout:**
```
+------------------------------------------+
| 🔢 Thần Số Học                          |
|------------------------------------------|
| [Họ và Tên] [Ngày sinh: DD/MM/YYYY]     |
| [Tính Số Mệnh 🔮]                       |
|------------------------------------------|
| 🌟 Life Path: 7 – Nhà tư tưởng sâu sắc   |
| 💬 Soul Urge: 9 – Tấm lòng nhân ái       |
| 🧭 Personality: 3 – Cởi mở, sáng tạo      |
|------------------------------------------|
| [Lưu kết quả] [Chia sẻ 🌠]              |
+------------------------------------------+
```

---

### 🌙 Zodiac Page
**UI Flow:** Input ngày sinh → Hiển thị cung hoàng đạo.

**Kết quả:**  
- Cung: ♏ Scorpio  
- Element: Water  
- Lucky Color: Deep Blue  
- Compatible Signs: Pisces, Cancer

**Hiệu ứng:** Nền gradient theo element, chòm sao chuyển động nhẹ.

---

### 💘 LoveMatch Page
```
+--------------------------------------------------+
| 💞 Bói Tình Duyên                               |
|--------------------------------------------------|
| [Tên bạn] [Ngày sinh bạn]                       |
| [Tên người ấy] [Ngày sinh người ấy]             |
| [Xem độ hợp 💘]                                 |
|--------------------------------------------------|
| ❤️ Compatibility: 87%                            |
| “Hai bạn có năng lượng tương hợp mạnh mẽ...”   |
| [Chia sẻ 💌]                                    |
+--------------------------------------------------+
```

Hiệu ứng: Trái tim đập theo % hợp đôi, particle bay ra thành hình trái tim.

---

### 🔮 Tarot Page
Deck 22 lá bài, chọn 3 lá → flip animation.  
Hiển thị:
```
Card 1 (Past) – The Tower ⚡  
Card 2 (Present) – The Lovers 💞  
Card 3 (Future) – The Star 🌟
```
> 💬 “Dù hiện tại hỗn loạn, ánh sáng vẫn đến.”

---

### 🌈 Daily Fortune Page
Card: Gradient pastel thay đổi mỗi ngày.
```
🌟 “Hôm nay, bạn sẽ nhận một món quà bất ngờ.”
🎨 Lucky Color: Gold
✨ Quote: “Kindness always returns.”
```

---

### 📜 History Page
Hiển thị danh sách kết quả bói.
```
📅 [20 Oct 2025] - Tarot Reading
Summary: The Lovers + The Star
[🔍 Xem lại]  [🗑️ Xóa]
```

---

### ⚙️ Settings Page
Form:  
- Avatar  
- Tên, Ngày sinh  
- Theme chọn (💜 Galaxy / 💙 Nebula / 💛 Sunrise)  
- Logout.

---

## 💫 4. Animation & Interaction
| Thành phần | Hiệu ứng |
|-------------|-----------|
| Button | Hover glow, pulse khi click |
| ResultCard | Fade-in + floating stars |
| TarotCard | Flip 3D |
| Navigation | Smooth slide transition |
| Background | Particle motion |

---

## 📱 5. Responsive Layout
- Mobile: 1 cột, scroll dọc
- Tablet: 2 cột
- Desktop: 3–4 cột
- Header collapsible trên mobile

---

## 🧠 6. UX Guideline
- **Principles:** Clarity, Delight, Consistency.  
- **Empty state:** “Bạn chưa xem bói nào hôm nay ✨ Hãy thử bói tarot xem sao!”  
- **Feedback:** Toast thông báo khi lưu / chia sẻ / tính toán thành công.

---

## 🧩 7. Component Library
| Component | Dùng để |
|------------|----------|
| `<Card />` | hiển thị kết quả |
| `<GlowButton />` | nút sáng động |
| `<StarBackground />` | hiệu ứng sao |
| `<ResultModal />` | popup kết quả |
| `<ShareCard />` | tạo ảnh chia sẻ |
| `<TarotCard />` | hiển thị lá tarot |
| `<ThemeSwitcher />` | chuyển theme |

---

## ✨ 8. Màu & Font chuẩn (Design Tokens)
| Token | Value |
|--------|--------|
| `--color-bg` | #0f0c29 |
| `--color-bg-gradient` | linear-gradient(45deg, #0f0c29, #302b63, #24243e) |
| `--color-primary` | #8A2BE2 |
| `--color-secondary` | #FFD700 |
| `--color-accent` | #E0B0FF |
| `--font-primary` | Quicksand |
| `--font-display` | Cinzel Decorative |
