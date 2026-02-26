content = """# 🏨 NexStay - Premium Property Reservation Platform

A full-stack property reservation platform inspired by DoubleTree by Hilton, built with Django REST Framework and Next.js.

![Django](https://img.shields.io/badge/Django-5.0-green)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🚀 Tech Stack

### Backend
- **Django 5.0** + Django REST Framework
- **SQLite** (development) / **PostgreSQL** (production)
- **JWT Authentication** via SimpleJWT
- **django-axes** - Brute force protection
- **django-guardian** - Object-level permissions
- **drf-spectacular** - Swagger UI auto docs
- **CORS** support

### Frontend
- **Next.js 14** (App Router + TypeScript)
- **Tailwind CSS**
- **Zustand** - Auth state management
- **Axios** - HTTP client with JWT interceptors
- **react-hot-toast** - Notifications

---

## ✨ Features

- 🔐 JWT Authentication (register, login, refresh)
- 🏠 Property listing & detail pages
- 🛏️ Multiple room types with amenities
- 📅 Real-time booking with price calculation
- 💳 8+ payment methods (QRIS, GoPay, OVO, DANA, etc.)
- 🌐 OTA integration (Booking.com, Agoda, Traveloka, Tiket.com)
- 📊 User dashboard (reservations & payments)
- 🏅 Loyalty program (Member, Silver, Gold, Diamond)
- 💰 Dynamic pricing by season
- 🎁 Discount coupon system
- ❌ Flexible cancellation policies
- ⭐ Guest review system
- 🛡️ Brute force & CSRF protection

---

## 📁 Project Structure

```
nexstay/
├── backend/
│   ├── config/         # Settings & URLs
│   ├── accounts/       # Auth & profiles
│   ├── properties/     # Room types & units
│   ├── reservations/   # Booking management
│   ├── payments/       # OTA, loyalty, pricing
│   ├── reviews/        # Guest reviews
│   └── requirements.txt
└── frontend/
    ├── app/            # Next.js pages
    ├── components/     # Navbar, Footer
    ├── lib/            # Axios client
    ├── store/          # Zustand store
    └── types/          # TypeScript types
```

---

## ⚙️ Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

### Frontend
```bash
cd frontend
npm install
# Set NEXT_PUBLIC_API_URL in .env.local
npm run dev
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register/ | Register |
| POST | /api/auth/login/ | Login JWT |
| GET | /api/auth/profile/ | User profile |
| GET | /api/properties/types/ | Room list |
| GET | /api/properties/types/{slug}/ | Room detail |
| GET/POST | /api/reservations/ | Reservations |
| GET | /api/payments/ | Payments |
| GET | /api/loyalty/ | Loyalty account |

Swagger UI: http://localhost:8000/api/docs/

---

## 💳 Payment Methods

Credit Card, Debit Card, QRIS, GoPay, OVO, DANA, Virtual Account, Bank Transfer, Cash

---

## 🌐 OTA Channels

Direct, Booking.com, Expedia, Agoda, Traveloka, Tiket.com, PegiPegi, Trip.com, Airbnb

---

## 🏅 Loyalty Tiers

| Tier | Points | Perks |
|------|--------|-------|
| Member | 0 | Basic discount |
| Silver | 5,000 | Free breakfast |
| Gold | 15,000 | Upgrade + late checkout |
| Diamond | 50,000 | Butler + airport transfer |

---

## 📄 License

MIT License

---
"""