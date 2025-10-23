# Email/Password Authentication

## Overview
Tính năng đăng nhập bằng Email/Password đã được thêm vào FateVerse, bổ sung cho phương thức đăng nhập Google OAuth hiện có.

## Features Implemented

### Backend (FastAPI)

1. **Password Hashing Utilities** (`backend/app/utils/password.py`)
   - `hash_password(password: str)`: Hash password using bcrypt
   - `verify_password(plain_password: str, hashed_password: str)`: Verify password

2. **Authentication Endpoints** (`backend/app/routes/auth.py`)
   - `POST /api/auth/register`: Register with email, password, and name
   - `POST /api/auth/login`: Login with email and password

3. **Database Model Updates** (`backend/app/models/user.py`)
   - Added `hashed_password` field to `UserInDB` model
   - `password` field in `UserCreate` for registration

### Frontend (React + TypeScript)

1. **API Client** (`frontend/src/utils/api.ts`)
   - `emailLogin(email, password)`: Call login endpoint
   - `emailRegister(data)`: Call register endpoint

2. **Auth Context** (`frontend/src/contexts/AuthContext.tsx`)
   - `loginWithEmail(email, password)`: Handle email login flow
   - `registerWithEmail(data)`: Handle registration flow

3. **Login UI** (`frontend/src/pages/LoginPage.tsx`)
   - Tabbed interface for Login/Register modes
   - Email and password input fields
   - Form validation
   - Integration with Google OAuth (divider: "hoặc tiếp tục với")

## How to Test

### 1. Start the Backend
```bash
cd backend
# Make sure environment variables are set (GOOGLE_CLIENT_ID, MONGODB_URI, etc.)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start the Frontend
```bash
cd frontend
npm run dev
```

### 3. Test Registration
1. Go to http://localhost:5173/login
2. Click "Đăng ký" tab
3. Fill in:
   - Tên của bạn: "Test User"
   - Email: "test@example.com"
   - Mật khẩu: "password123"
   - Xác nhận mật khẩu: "password123"
4. Click "Đăng ký ngay"
5. Should redirect to home page with user logged in

### 4. Test Login
1. Go to http://localhost:5173/login
2. Click "Đăng nhập" tab
3. Fill in:
   - Email: "test@example.com"
   - Mật khẩu: "password123"
4. Click "Đăng nhập"
5. Should redirect to home page with user logged in

### 5. Test Error Cases

#### Duplicate Email Registration
1. Try to register with the same email again
2. Should show error: "Email đã được đăng ký"

#### Wrong Password
1. Try to login with wrong password
2. Should show error: "Email hoặc mật khẩu không đúng"

#### Password Mismatch
1. Register with different passwords in password/confirm fields
2. Should show error: "Mật khẩu xác nhận không khớp"

#### Short Password
1. Register with password < 6 characters
2. Should show error: "Mật khẩu phải có ít nhất 6 ký tự"

#### Google Account Login Attempt
1. Login with Google first (create account)
2. Logout
3. Try to login with email/password using same email
4. Should show error: "Tài khoản này đã đăng ký bằng Google. Vui lòng đăng nhập bằng Google."

## Security Features

1. **Password Hashing**: Passwords are hashed using bcrypt with automatic salt generation
2. **JWT Tokens**: 30-day expiration, stored in localStorage
3. **Account Type Protection**: Prevents password login on Google-only accounts
4. **Input Validation**: Email format validation, password length requirements
5. **Error Messages**: User-friendly Vietnamese error messages

## Database Schema

Users collection now includes:
```json
{
  "id": "ObjectId",
  "email": "user@example.com",
  "name": "User Name",
  "hashed_password": "$2b$12$...",  // Optional (only for email/password users)
  "google_id": "google_user_id",     // Optional (only for Google users)
  "picture": "https://...",
  "theme_preference": "galaxy",
  "created_at": "2024-01-01T00:00:00",
  "last_login": "2024-01-01T00:00:00",
  "birth_date": "1990-01-01",        // Optional
  "gender": "male"                    // Optional
}
```

## API Endpoints

### POST /api/auth/register
**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "User Name",
  "birth_date": "1990-01-01",  // Optional
  "gender": "male"              // Optional
}
```

**Response:**
```json
{
  "user": {
    "id": "...",
    "name": "User Name",
    "email": "user@example.com",
    "picture": "",
    "theme_preference": "galaxy",
    "created_at": "2024-01-01T00:00:00"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Đăng ký thành công"
}
```

### POST /api/auth/login
**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "user": {
    "id": "...",
    "name": "User Name",
    "email": "user@example.com",
    "picture": "",
    "theme_preference": "galaxy",
    "created_at": "2024-01-01T00:00:00"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Đăng nhập thành công"
}
```

## Next Steps (Optional Enhancements)

1. **Password Reset**: Add forgot password functionality with email
2. **Email Verification**: Send verification email on registration
3. **Password Strength Indicator**: Visual feedback on password strength
4. **Remember Me**: Optional longer token expiration
5. **Two-Factor Authentication**: Add 2FA support
6. **Social Login**: Add Facebook, Apple, etc.
7. **Profile Picture Upload**: Allow users to upload custom avatars
