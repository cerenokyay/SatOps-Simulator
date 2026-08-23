from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Veritabanı Bağlantı Ayarları (SQLite)
DATABASE_URL = "sqlite:///./telemetry.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Veritabanı Tablo Modeli
class TelemetryRecord(Base):
    __tablename__ = "telemetry"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String, index=True)
    voltage = Column(Float)
    temperature = Column(Float)

# Tabloları oluştur
Base.metadata.create_all(bind=engine)

# 3. FastAPI Uygulaması
app = FastAPI(title="SatOps Ground Station")

class TelemetryData(BaseModel):
    voltage: float
    temperature: float

@app.post("/telemetry")
async def receive_telemetry(data: TelemetryData):
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # 4. Gelen veriyi veritabanına kaydet
    db = SessionLocal()
    db_record = TelemetryRecord(timestamp=timestamp, voltage=data.voltage, temperature=data.temperature)
    db.add(db_record)
    db.commit()
    db.close()
    
    print(f"[{timestamp}] 🛰️ DB'YE KAYDEDİLDİ -> Voltaj: {data.voltage:.2f}V | Sıcaklık: {data.temperature:.2f}°C")
    return {"status": "success", "message": "Telemetri kaydedildi"}