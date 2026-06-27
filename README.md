# ⚙️ Meta Earth Vietnam — Backend

Backend API cho hệ thống **Meta Earth Việt Nam**. Xây dựng trên FastAPI với MongoDB, phục vụ toàn bộ logic nghiệp vụ bao gồm xác thực, quản lý đăng ký người dùng, tin tức, và giá MEC token.

🚀 **Production:** [meta-earth-backend.onrender.com](https://meta-earth-backend.onrender.com)

---

## Tech Stack

| Công nghệ | Vai trò |
|---|---|
| Python | Ngôn ngữ chính |
| FastAPI | Web framework |
| Beanie ODM | MongoDB ORM (async) |
| MongoDB | Database |
| PyMongo | MongoDB driver |
| python-jose | JWT authentication |
| passlib + bcrypt | Password hashing |
| Pydantic | Data validation |
| Uvicorn | ASGI server |

---

## Cấu trúc dự án

```
meta-earth-backend/
├── main.py                    # Entry point — FastAPI app + router registration
├── create_admin.py            # Script tạo tài khoản admin
├── requirements.txt           # Python dependencies
├── runtime.txt                # Python version (cho Render)
└── app/
    ├── core/
    │   ├── config.py          # Cấu hình môi trường (.env)
    │   ├── database.py        # Kết nối MongoDB
    │   └── security.py        # JWT + password hashing
    ├── models/
    │   ├── user.py            # Model User
    │   ├── registration.py    # Model Registration (đăng ký pending)
    │   ├── blacklist_email.py # Model Blacklist Email
    │   ├── blacklist_wallet.py# Model Blacklist Wallet
    │   ├── news.py            # Model NewsItem
    │   └── mec_price.py       # Model MECPrice
    ├── routers/
    │   ├── auth.py            # POST /api/v1/login
    │   ├── admin.py           # Admin routes (protected)
    │   ├── registration.py    # Đăng ký người dùng mới
    │   ├── news.py            # CRUD tin tức
    │   └── mec_price.py       # Giá MEC token
    └── schemas/
        ├── registration.py    # Pydantic schemas cho registration
        └── news.py            # Pydantic schemas cho news
```

---

## API Endpoints

### Auth
| Method | Endpoint | Mô tả |
|---|---|---|
| POST | `/api/v1/login` | Đăng nhập, trả về JWT token |

### Admin *(yêu cầu JWT — role: admin)*
| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/api/v1/admin/registrations` | Xem danh sách đăng ký pending |
| POST | `/api/v1/admin/grant/{id}` | Duyệt đăng ký, tạo user + gửi password |
| POST | `/api/v1/admin/decline/{id}` | Từ chối + blacklist ví & email |

### Registration
| Method | Endpoint | Mô tả |
|---|---|---|
| POST | `/api/v1/registration` | Submit đăng ký mới |

### News & Price
| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/api/v1/news` | Lấy danh sách tin tức |
| GET | `/api/v1/mec-price` | Lấy giá MEC token hiện tại |

---

## Chạy local

**Yêu cầu:** Python >= 3.11, MongoDB

```bash
# Clone repo
git clone https://github.com/OliverWong0301/meta-earth-backend.git
cd meta-earth-backend

# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Cài dependencies
pip install -r requirements.txt

# Tạo file .env (xem mẫu bên dưới)
# Tạo tài khoản admin (lần đầu)
python create_admin.py

# Chạy server
uvicorn main:app --reload
```

API docs tại [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Cấu hình môi trường (.env)

Tạo file `.env` ở thư mục gốc với nội dung:

```env
MONGO_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net
DATABASE_NAME=meta_earth_db
```

> ⚠️ **Không commit file `.env` lên GitHub.** Đã được thêm vào `.gitignore`.

---

## Deployment

Backend được deploy trên **Render** (free tier). Mỗi lần push lên `main`, Render tự động redeploy.

> ⚠️ **Workflow quan trọng:** Code phải được test local và xác nhận OK trước khi push lên GitHub.

---

## User Flow — Registration & Admin

```
User submit đăng ký (ví MePass + ảnh MeID + email)
    ↓
Hệ thống lưu với status: PENDING
    ↓
Admin review trên Dashboard
    ↓
┌─────────────┬──────────────────────────────┐
│   GRANT     │           DECLINE            │
│             │                              │
│ Tạo User    │ Blacklist wallet + email     │
│ Random pass │ Gửi email từ chối            │
│ Gửi email   │                              │
└─────────────┴──────────────────────────────┘
```

---

## Frontend

- **Production:** [meta-earth-vietnam.vercel.app](https://meta-earth-vietnam.vercel.app)
- **Repo:** [meta-earth-vietnam](https://github.com/OliverWong0301/meta-earth-vietnam)

---

## Roadmap Backend

| Phase | Việc cần làm |
|---|---|
| ✅ Done | Auth JWT, Admin Grant/Decline, Blacklist, Login |
| 🔄 Next | Đổi mật khẩu user, chuẩn hóa error handling |
| ⏳ Soon | Tích hợp MePass Wallet, gửi email tự động |
| 📋 Later | DAO features, Proposal, Voting, Treasury |