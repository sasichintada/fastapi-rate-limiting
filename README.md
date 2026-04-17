
---

## 📌 FastAPI Rate Limiting Service

A backend system built with **FastAPI** that provides **API Key Authentication, Rate Limiting, and Usage Tracking** using SQLite.

---

## 🚀 Features

* 🔐 API Key Authentication (UUID-based)
* 🧾 Client tracking (name, email, timestamps)
* 🚦 Rate Limiting (5 requests/min per key)
* 📊 Usage tracking (total + endpoint-wise)
* 🔒 Protected APIs requiring API key
* ❌ HTTP 429 on limit exceed
* 📖 Swagger UI (`/docs`)

---

## 🏗️ Project Structure

```text id="struct1"
app/
│── main.py
│
├── api/
│   ├── auth.py
│   ├── protected.py
│
├── core/
│   ├── config.py
│   ├── dependencies.py
│   ├── rate_limiter.py
│
├── database/
│   ├── database.py
│
├── models/
│   ├── api_key.py
│   ├── usage.py
│
├── services/
│   ├── api_key_service.py
│   ├── usage_service.py
```

---

## ⚙️ Tech Stack

* FastAPI
* SQLite (SQLAlchemy)
* Pydantic
* Uvicorn
* Python 3.11

---

## 🔧 Setup

```bash id="setup1"
git clone https://github.com/sasichintada/fastapi-rate-limiting.git
cd fastapi-rate-limiting

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## 🌐 API Docs

```
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication

### Generate API Key

```
POST /auth/generate-key
```

### Header (Required)

```
X-API-Key: <your_api_key>
```

---

## 📡 API ENDPOINTS

### 🔐 Auth APIs

| Method | Endpoint               | Description      |
| ------ | ---------------------- | ---------------- |
| POST   | /auth/generate-key     | Generate API key |
| GET    | /auth/usage-stats      | Usage statistics |
| POST   | /auth/revoke-key/{key} | Revoke key       |
| GET    | /auth/list-keys        | List keys        |

---

### 🔒 Protected APIs

| Method | Endpoint            | Description  |
| ------ | ------------------- | ------------ |
| GET    | /api/protected-data | Secure data  |
| GET    | /api/user-info      | User info    |
| POST   | /api/process-data   | Process data |

---

## 🚦 Rate Limiting

* Limit: **5 requests/min per API key**
* Exceed → `429 Too Many Requests`

```json id="rate1"
{
  "detail": "Rate limit exceeded. Try again later.",
  "status_code": 429
}
```

---

## 📊 Usage Tracking

```
GET /auth/usage-stats?hours=24
```

Returns:

* Total requests
* Endpoint breakdown

---

## 📌 Flow

Generate Key → Use Header → Call API → Track Usage → Rate Limit Enforced

---

## 👨‍💻 Author

**Sasi Chintada**
* GitHub: @sasichintada

---

