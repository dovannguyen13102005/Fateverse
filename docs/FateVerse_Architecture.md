# 🏗️ FateVerse – Architecture Design (ERD + 4C Model)

---

## 🌌 A. Entity Relationship Diagram (ERD)

### 🧩 Tổng quan
FateVerse có 5 mô-đun chính: Thần số học, Chiêm tinh, Tình duyên, Tarot, Daily Fortune cùng hệ thống user + lịch sử.

### 🗺️ ERD
```
┌──────────────────────┐
│        User          │
├──────────────────────┤
│ user_id (PK)         │
│ name                 │
│ email                │
│ birth_date           │
│ gender               │
│ theme_preference     │
│ created_at           │
└────────┬─────────────┘
         │ 1..*
         ▼
┌──────────────────────┐
│   FortuneHistory     │
├──────────────────────┤
│ fortune_id (PK)      │
│ user_id (FK → User)  │
│ type (ENUM: tarot/love/zodiac/numerology/daily) │
│ result_summary        │
│ result_detail (JSON) │
│ created_at           │
└────────┬─────────────┘
         │
         ├───────────────────────────────────────┐
         ▼                                       ▼
┌──────────────────────┐             ┌──────────────────────┐
│     TarotCard        │             │     LoveMatch        │
├──────────────────────┤             ├──────────────────────┤
│ card_id (PK)         │             │ match_id (PK)        │
│ name                 │             │ user_id (FK → User)  │
│ meaning              │             │ partner_name         │
│ image_url            │             │ partner_birth_date   │
│ category (love/work) │             │ compatibility_score  │
└──────────────────────┘             │ analysis_text        │
                                    └──────────────────────┘
         │
         ▼
┌──────────────────────┐
│     ZodiacData       │
├──────────────────────┤
│ zodiac_id (PK)       │
│ name                 │
│ element              │
│ description          │
│ lucky_number         │
│ lucky_color          │
│ compatible_signs     │
└──────────────────────┘

┌──────────────────────┐
│   NumerologyResult   │
├──────────────────────┤
│ numerology_id (PK)   │
│ user_id (FK → User)  │
│ life_path_number     │
│ expression_number    │
│ soul_urge_number     │
│ personality_number   │
│ analysis_text        │
└──────────────────────┘

┌──────────────────────┐
│   DailyFortune       │
├──────────────────────┤
│ fortune_date (PK)    │
│ message              │
│ lucky_color          │
│ emoji                │
│ quote                │
└──────────────────────┘
```

💡 **Giải thích:**
- `User` là trung tâm.  
- Mọi kết quả bói lưu trong `FortuneHistory`.  
- Các bảng `TarotCard`, `ZodiacData`, `DailyFortune` chứa dữ liệu mẫu.  
- Bảng `NumerologyResult` & `LoveMatch` chứa kết quả tính toán chi tiết.

---

## 🧱 B. 4C Model Architecture

### 1️⃣ Context Level
FateVerse là một web app xem bói đa dạng, cho phép người dùng xem thần số học, cung hoàng đạo, tình duyên, tarot, lá số mỗi ngày.

**Actor:**
- 👤 User: sử dụng app
- 🤖 System (FateVerse): xử lý logic bói toán
- ☁️ AI / Data Source: cung cấp mô tả, giải nghĩa, dữ liệu chòm sao hoặc lá bài.

### Data Flow
1. User → Frontend → chọn loại bói  
2. Frontend gọi API tương ứng  
3. Backend xử lý logic → truy xuất DB hoặc AI  
4. Trả kết quả → UI hiển thị + animation  

---

### 2️⃣ Container Level
| Container | Technology | Purpose |
|------------|-------------|----------|
| 🌐 Frontend | React + Tailwind + Framer Motion | UI, routing, animation |
| ⚙️ Backend API | FastAPI (Python) hoặc Express.js (Node) | Xử lý logic & API endpoints |
| 🗄️ Database | MongoDB Atlas / Firebase Firestore | Lưu trữ dữ liệu & kết quả |
| 🔮 AI / Utility Layer | OpenAI / Gemini API | Sinh mô tả, giải nghĩa chi tiết |
| ☁️ Hosting | Vercel (frontend), Render/Fly.io (backend) | Deploy hệ thống |
| 🔑 Auth Provider | Firebase Auth / Google OAuth | Đăng nhập & xác thực |

---

### 3️⃣ Component Level
**Frontend Components**
| Component | Description |
|------------|-------------|
| `HomePage.jsx` | Trang chủ, giới thiệu 5 loại bói |
| `NumerologyPage.jsx` | Tính thần số học |
| `ZodiacPage.jsx` | Cung hoàng đạo |
| `LoveMatchPage.jsx` | Bói hợp đôi |
| `TarotPage.jsx` | Giao diện rút bài |
| `DailyFortune.jsx` | Fortune mỗi ngày |
| `HistoryPage.jsx` | Lịch sử kết quả |
| `SettingsPage.jsx` | Cài đặt, theme |
| `ResultCard.jsx` | Kết quả share được |

**Backend Modules**
| Module | Endpoint | Function |
|---------|-----------|----------|
| `auth.py` | `/api/auth` | Xử lý đăng nhập |
| `numerology.py` | `/api/numerology` | Tính thần số học |
| `zodiac.py` | `/api/zodiac` | Xác định cung hoàng đạo |
| `love.py` | `/api/love` | Tính hợp đôi |
| `tarot.py` | `/api/tarot` | Rút bài Tarot |
| `fortune.py` | `/api/fortune` | Lá số hôm nay |
| `history.py` | `/api/history` | Quản lý lịch sử |
| `ai_helper.py` | `/api/ai/explain` | Gọi AI để sinh mô tả |

---

### 4️⃣ Code Level (Implementation)
```
/fateverse
 ├── frontend/
 │   ├── src/
 │   │   ├── components/
 │   │   ├── pages/
 │   │   ├── styles/
 │   │   ├── utils/
 │   │   └── main.jsx
 │   └── public/
 │       └── tarot_images/
 │
 ├── backend/
 │   ├── main.py
 │   ├── routes/
 │   ├── models/
 │   ├── services/
 │   ├── database/
 │   └── utils/
 │
 ├── .env
 ├── requirements.txt
 └── README.md
```

---

### 💡 Tổng kết
| Mô hình | Mục tiêu |
|----------|-----------|
| **ERD** | Định nghĩa dữ liệu & quan hệ giữa mô-đun |
| **4C** | Kiến trúc tổng thể, đảm bảo khả năng mở rộng & maintain |
