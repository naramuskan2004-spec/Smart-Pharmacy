# Smart Pharmacy

A FastAPI-based inventory management system that uses QR codes for product tracking.

## Features

* Add products to inventory
* View inventory
* Delete products
* Generate QR codes
* Scan QR codes
* Smart QR auto-add
* Expiry alerts
* SQLite database integration

## Technology Stack

* Python
* FastAPI
* SQLAlchemy
* SQLite
* PyZbar
* Pillow
* Uvicorn

## Project Structure

backend/
├── app/
│ ├── main.py
│ ├── models.py
│ ├── schemas.py
│ └── database.py
├── generate_qr.py
└── pharmacy.db

## Run the Project

1. Create virtual environment

```bash
python -m venv venv
```

2. Activate virtual environment

```bash
venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Start server

```bash
uvicorn app.main:app --reload
```

Swagger UI:

http://127.0.0.1:8000/docs

