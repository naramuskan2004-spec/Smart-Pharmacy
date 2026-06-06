from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    batch_number = Column(String)
    manufacturer = Column(String)
    mfg_date = Column(Date)
    exp_date = Column(Date)
    quantity = Column(Integer)