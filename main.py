from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime

app = FastAPI()

try:
    client = MongoClient("mongodb+srv://darkphoenix67cdlc:wrqxPT5KduwcQHZ0@registros.l1xvkg8.mongodb.net/?retryWrites=true&w=majority&appName=Registros")
    client.server_info()
    db = client["Registros"]
    collection = db["localizaciones"]
    print("✅ Conectado correctamente a MongoDB Atlas")
except Exception as e:
    print("❌ Error al conectar con MongoDB:", e)

class Checkin(BaseModel):
    nombre: str
    lat: float
    lng: float

@app.post("/checkin")
def recibir_checkin(data: Checkin):
    now = datetime.now()

    registro = {
        "nombre": data.nombre,
        "latitud": data.lat,
        "longitud": data.lng,
        "hora": now.strftime("%H:%M"),
        "dia": now.day,
        "mes": now.month,
        "año": now.year
    }

    collection.insert_one(registro)
    print(f"✅ Check-in recibido de {data.nombre} a las {registro['hora']} ({registro['latitud']}, {registro['longitud']})")

    return {"mensaje": f"Check-in de {data.nombre} guardado correctamente"}