# Smart Pharmacy Inventory System
A backend system that manages pharmacy inventory using FastAPI, SQLite, and QR codes.
It enables smart tracking of medicines, expiry dates, and stock levels through QR-based identification.

# Features
•	Add and manage medicines in inventory
•	QR code generation for each medicine
•	Scan QR to retrieve medicine details instantly
•	Track expiry dates of medicines
•	Basic stock and expiry monitoring system
•	FastAPI-based RESTful backend
•	SQLite database for lightweight storage


# Tech Stack
Python
FastAPI
SQLite
Pydantic
QR Code (qrcode library)


# Installation & Setup
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn app.main:app --reload

# API Documentation

After running the project:

http://127.0.0.1:8000/docs

# Screenshots
<img width="1871" height="528" alt="scan-qr-smart" src="https://github.com/user-attachments/assets/8cbbe6e8-1f28-41ab-80c3-72d0b830d1e6" />
<img width="1865" height="712" alt="scan-qr-response" src="https://github.com/user-attachments/assets/e712a60b-217b-444f-bd34-12912ae486fe" />
<img width="1917" height="971" alt="Fast API" src="https://github.com/user-attachments/assets/a11c6705-c249-4fa2-962c-e79c5278ae04" />

