# 🏋️‍♀️ Fitness Studio Booking API

A simple Booking API for a fictional fitness studio built with **Python**, **Django**, and **Django REST Framework**.

## Documentation

Detailed project documentation is available [here](https://tejaswitaw.github.io/fitness_studio/).


## 🚀 Features

- View upcoming fitness classes
- Book a class (with slot validation)
- View bookings for a specific client
- Seed the database with sample data
- Filter classes by time zone

---

## 🛠️ Tech Stack

- **Python 3.12**
- **Django 5.2.2**
- **Django REST Framework 3.16.0**
- **Postman** (for API testing)

---
## 📂 Getting Started

## 🔁 Clone the Repository

```bash
git clone https://github.com/TejaswitaW/fitness_studio.git
cd fitness_studio
```

## 🧱 Set Up Virtual Environment

```bash
python -m venv venv
```

## ▶️ Activate the Environment


On **Windows**:
```bash
.\venv\Scripts\activate
```

On **macOS/Linux**:
```bash
source venv/bin/activate
```

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

## 🔄 Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 🌱 Seed Fake Data

```bash
python manage.py seed_data
```

## ▶️ Run the Server

```bash
python manage.py runserver
Server will run at: http://127.0.0.1:8000
```
## 🧪 Running Tests

```bash
python manage.py pytest
```


## 📬 API Endpoints

All endpoints are prefixed with `/api/`

## ✅ View All Upcoming Classes

**GET** `/api/classes/`  

🔗 **Example:** [http://127.0.0.1:8000/api/classes/](http://127.0.0.1:8000/api/classes/)

Optional: filter by time zone 

**GET** `/api/classes/?timezone=America/New_York`

## 📝 Book a Class

**POST** `/api/book/`

**Request Body Example (JSON):**

```json
{
    "class_id": 2,
    "client_name": "John",
    "client_email": "john@gmail.com"
}
```
🔗 **Example:** [http://127.0.0.1:8000/api/book/](http://127.0.0.1:8000/api/book/)

## 📒 View Bookings by Email

**GET** `/api/bookings/?email=<email>`

🔗 **Example:** [http://127.0.0.1:8000/api/bookings/?email=abc@gmail.com](http://127.0.0.1:8000/api/bookings/?email=abc@gmail.com)



## 👥 View All Clients

**GET** `/api/clients/`

🔗 **Example:** [http://127.0.0.1:8000/api/clients/](http://127.0.0.1:8000/api/clients/)

## 🔍 API Testing Tool

All endpoints can be tested using **Postman** or any other REST client of your choice.



## 👩‍💻 Author

**Tejaswita Wakhure**  

Feel free to connect or contribute!
