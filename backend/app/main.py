from fastapi import FastAPI, Depends, UploadFile, File
from PIL import Image
from pyzbar.pyzbar import decode
import io
import json
from datetime import datetime
from datetime import date, timedelta
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.models import Base, Medicine
from app.schemas import MedicineCreate, DeleteMedicines

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Smart Pharmacy API Running"}

@app.post("/medicines")
def add_medicine(
    medicine: MedicineCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Medicine).filter(
        Medicine.batch_number == medicine.batch_number
    ).first()

    if existing:
        return {
            "message": f"Batch number {medicine.batch_number} already exists"
        }

    new_medicine = Medicine(
        product_name=medicine.product_name,
        batch_number=medicine.batch_number,
        manufacturer=medicine.manufacturer,
        mfg_date=medicine.mfg_date,
        exp_date=medicine.exp_date,
        quantity=medicine.quantity
    )

    db.add(new_medicine)
    db.commit()
    db.refresh(new_medicine)

    return {
        "message": "Medicine added successfully",
        "id": new_medicine.id
    }
@app.get("/medicines")
def get_medicines(db: Session = Depends(get_db)):
    medicines = db.query(Medicine).all()
    return medicines
@app.get("/count")
def medicine_count(db: Session = Depends(get_db)):
    total = db.query(Medicine).count()

    return {
        "total_medicines": total
    }
@app.delete("/medicines/{medicine_id}")
def delete_medicine(
    medicine_id: int,
    db: Session = Depends(get_db)
):
    medicine = db.query(Medicine).filter(
        Medicine.id == medicine_id
    ).first()

    if not medicine:
        return {"message": "Medicine not found"}

    db.delete(medicine)
    db.commit()

    return {"message": "Medicine deleted"}
@app.post("/medicines/delete-many")
def delete_multiple_medicines(
    data: DeleteMedicines,
    db: Session = Depends(get_db)
):
    deleted = 0

    for medicine_id in data.ids:
        medicine = db.query(Medicine).filter(
            Medicine.id == medicine_id
        ).first()

        if medicine:
            db.delete(medicine)
            deleted += 1

    db.commit()

    return {
        "message": f"{deleted} medicines deleted"
    }
@app.post("/scan-qr")
async def scan_qr(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()

    image = Image.open(io.BytesIO(contents))

    decoded_objects = decode(image)

    if not decoded_objects:
        return {"message": "No QR code found"}

    qr_data = decoded_objects[0].data.decode("utf-8")

    data = json.loads(qr_data)

    batch_number = data["batch_number"]

    medicine = db.query(Medicine).filter(
        Medicine.batch_number == batch_number
    ).first()

    if not medicine:
        return {"message": "Medicine not found"}

    return {
        "id": medicine.id,
        "product_name": medicine.product_name,
        "batch_number": medicine.batch_number,
        "manufacturer": medicine.manufacturer,
        "mfg_date": medicine.mfg_date,
        "exp_date": medicine.exp_date,
        "quantity": medicine.quantity
    }


@app.post("/scan-qr-add")
async def scan_qr_add(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()

    image = Image.open(io.BytesIO(contents))

    decoded_objects = decode(image)

    if not decoded_objects:
        return {"message": "No QR code found"}

    qr_data = decoded_objects[0].data.decode("utf-8")

    data = json.loads(qr_data)

    print("QR DATA:")
    print(data)

    # Flexible field mapping

    product_name = (
        data.get("product_name")
        or data.get("name")
        or "N/A"
    )

    batch_number = (
        data.get("batch_number")
        or data.get("batch_no")
        or data.get("batch")
        or "N/A"
    )

    manufacturer = (
        data.get("manufacturer")
        or data.get("company")
        or data.get("maker")
        or "N/A"
    )

    mfg = (
        data.get("mfg_date")
        or data.get("mfg")
        or data.get("manufacture_date")
        or "2000-01-01"
    )

    exp = (
        data.get("exp_date")
        or data.get("exp")
        or data.get("expiry")
        or data.get("expiry_date")
        or "2099-12-31"
    )

    quantity = data.get("quantity", 0)

    # Convert dates to Python date objects

    mfg_date = datetime.strptime(mfg, "%Y-%m-%d").date()
    exp_date = datetime.strptime(exp, "%Y-%m-%d").date()

    # Check duplicate batch number

    existing = db.query(Medicine).filter(
        Medicine.batch_number == batch_number
    ).first()

    if existing:
        return {
            "message": "Medicine already exists",
            "id": existing.id
        }

    # Create medicine

    new_medicine = Medicine(
        product_name=product_name,
        batch_number=batch_number,
        manufacturer=manufacturer,
        mfg_date=mfg_date,
        exp_date=exp_date,
        quantity=quantity
    )

    db.add(new_medicine)
    db.commit()
    db.refresh(new_medicine)

    return {
        "message": "Medicine added successfully",
        "id": new_medicine.id,
        "product_name": new_medicine.product_name,
        "batch_number": new_medicine.batch_number
    }
from datetime import date

@app.post("/scan-qr-smart")
async def scan_qr_smart(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()

    image = Image.open(io.BytesIO(contents))

    decoded_objects = decode(image)

    if not decoded_objects:
        return {"message": "No QR code found"}

    qr_data = decoded_objects[0].data.decode("utf-8")

    data = json.loads(qr_data)

    print("QR DATA:")
    print(data)

    batch_number = (
        data.get("batch_number")
        or data.get("batch_no")
        or data.get("batch")
        or "NA"
    )

    existing = db.query(Medicine).filter(
        Medicine.batch_number == batch_number
    ).first()

    if existing:
        return {
            "status": "exists",
            "id": existing.id,
            "product_name": existing.product_name,
            "batch_number": existing.batch_number
        }

    new_medicine = Medicine(
        product_name=data.get("product_name", "NA"),
        batch_number=batch_number,
        manufacturer=data.get("manufacturer", "NA"),
        mfg_date=date.fromisoformat(
            data.get("mfg_date", data.get("mfg", "2026-01-01"))
        ),
        exp_date=date.fromisoformat(
            data.get("exp_date", data.get("exp", "2027-01-01"))
        ),
        quantity=data.get("quantity", 0)
    )

    db.add(new_medicine)
    db.commit()
    db.refresh(new_medicine)

    return {
        "status": "added",
        "id": new_medicine.id,
        "product_name": new_medicine.product_name,
        "batch_number": new_medicine.batch_number
    }


@app.get("/expiry-alerts")
def expiry_alerts(db: Session = Depends(get_db)):

    today = date.today()
    next_30_days = today + timedelta(days=30)

    medicines = db.query(Medicine).all()

    expired = []
    expiring_soon = []
    safe = []

    for medicine in medicines:

        item = {
            "id": medicine.id,
            "product_name": medicine.product_name,
            "batch_number": medicine.batch_number,
            "exp_date": medicine.exp_date
        }

        if medicine.exp_date < today:
            expired.append(item)

        elif medicine.exp_date <= next_30_days:
            expiring_soon.append(item)

        else:
            safe.append(item)

    return {
        "expired_count": len(expired),
        "expiring_soon_count": len(expiring_soon),
        "safe_count": len(safe),
        "expired": expired,
        "expiring_soon": expiring_soon
    }