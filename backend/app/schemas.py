from pydantic import BaseModel
from datetime import date

class MedicineCreate(BaseModel):
    product_name: str
    batch_number: str
    manufacturer: str
    mfg_date: date
    exp_date: date
    quantity: int
class DeleteMedicines(BaseModel):
    ids: list[int]