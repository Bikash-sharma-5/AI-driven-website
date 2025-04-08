# 🧠 AI-Driven Website Builder (Django Backend)

This project powers a backend service that allows users to automatically generate customizable business websites using AI. Users can register, create websites based on their business type and industry, and preview them with a live temporary URL.

---

## 🚀 Features

- 🔐 **JWT Authentication** (Login/Register)
- 🏗️ **Create, Read, Update, Delete (CRUD)** Websites
- 🎨 **AI-generated website content** (via API integration)
- 🌐 **Live Preview** using unique `preview_token` links
- 📦 JSON-based content handling for dynamic rendering
- 📅 Timestamped website creation for user history tracking

---

## 🛠️ Tech Stack

- **Backend:** Django & Django REST Framework
- **Database:** MongoDb
- **Auth:** JWT (Simple JWT)
- **Frontend Preview :** HTML Template rendered using Django views

---

## 🗂️ Project Structure

ai_website_builder/ │ ├── builder/ # Main app │ ├── models.py # Website model │ ├── views.py # API & preview logic │ ├── serializers.py # DRF serializers │ ├── urls.py # App-specific routes │ ├── ai_website_builder/ # Project config │ ├── settings.py # Django settings │ ├── urls.py # Root URLs │ ├── templates/ # HTML templates for preview │ └── preview.html │ ├── manage.py ├── db.sqlite3 # SQLite DB └── requirements.txt

yaml
Copy
Edit

---

## 🧪 API Endpoints

| Method | Endpoint                     | Description                    |
|--------|------------------------------|--------------------------------|
| POST   | `/api/register/`             | Register a new user            |
| POST   | `/api/token/`                | Get JWT token                  |
| POST   | `/api/websites/`             | Create a new website           |
| GET    | `/api/websites/`             | Get all websites (user-wise)   |
| GET    | `/api/websites/<id>/`        | Get website by ID              |
| PUT    | `/api/websites/<id>/`        | Update website                 |
| DELETE | `/api/websites/<id>/`        | Delete website                 |
| GET    | `/preview/<token>/`          | View live website preview      |

---

## 🧰 Installation

```bash
# 1. Clone the Repository
git clone https://github.com/Bikash-sharma-5/AI-driven-website.git
cd AI-driven-website

# 2. Create Virtual Environment
python -m venv env
source env/bin/activate       # For Mac/Linux
# OR
env\Scripts\activate          # For Windows

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Run Migrations
python manage.py migrate

# 5. Run Server
python manage.py runserver
