import qrcode
import json

data = {
    "product_name": "Azithromycin",
    "batch_number": "AZ001",
    "manufacturer": "Sun Pharma",
    "mfg_date": "2026-06-01",
    "exp_date": "2028-06-01",
    "quantity": 20
}

img = qrcode.make(json.dumps(data))
img.save("azithromycin_qr.png")

print("QR created")