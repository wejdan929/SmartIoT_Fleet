from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os

# Initialisation de l'application FastAPI
app = FastAPI(
    title="SmartIoT Fleet - Predictive Maintenance API",
    description="API REST pour la prédiction d'anomalies sur les véhicules de la flotte IoT",
    version="1.0.0"
)

MODEL_PATH = "ml_model/model.pkl"

# Structure des données attendues en entrée (Pydantic)
class TelemetryData(BaseModel):
    speed_kmh: float
    engine_temp_c: float
    vibration_level: float

# Variable globale pour stocker le modèle chargé
model = None

@app.on_event("startup")
def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("✅ Modèle ML chargé avec succès dans l'API REST !")
    else:
        print("⚠️ Attention : Aucun fichier model.pkl trouvé.")

@app.get("/")
def read_root():
    return {
        "message": "Bienvenue sur l'API SmartIoT Fleet 🚚",
        "status": "online"
    }

@app.post("/predict")
def predict_status(data: TelemetryData):
    if model is None:
        raise HTTPException(status_code=500, detail="Modèle non disponible sur le serveur.")
    
    # Formatage des données pour la prédiction
    features = [[data.speed_kmh, data.engine_temp_c, data.vibration_level]]
    
    # Exécution de la prédiction
    prediction = model.predict(features)[0]
    
    return {
        "speed_kmh": data.speed_kmh,
        "engine_temp_c": data.engine_temp_c,
        "vibration_level": data.vibration_level,
        "predicted_status": prediction
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    