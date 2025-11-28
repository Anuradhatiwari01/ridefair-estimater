from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np

# Initialize the App
app = FastAPI(title="RideFair AI API", version="1.0")

# CORS SECURITY FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)


# LOAD THE TRAINED MODELS
try:
    with open("all_models.pkl", "rb") as f:
        models = pickle.load(f)
    
    price_model = models["price_model"]
    scam_model = models["scam_model"]
    hotspot_model = models["hotspot_model"]
    print("Models loaded successfully!")
except FileNotFoundError:
    print("ERROR: 'all_models.pkl' not found. Run train_ai.py first!")

#  DEFINE INPUT FORMATS
class PriceRequest(BaseModel):
    distance_km: float
    hour: int
    is_weekend: int

class ScamRequest(BaseModel):
    distance_km: float
    price_asked: float

#  API ENDPOINTS

@app.get("/")
def home():
    return {"message": "RideFair AI is Online."}

@app.post("/predict-price")
def predict_price(data: PriceRequest):
    features = pd.DataFrame([{
        'dist_km': data.distance_km,
        'hour': data.hour,
        'is_weekend': data.is_weekend
    }])
    
    predicted_price = price_model.predict(features)[0]
    
    return {
        "fair_price": round(predicted_price, 2),
        "message": "Calculated based on historical data."
    }

@app.post("/detect-scam")
def detect_scam(data: ScamRequest):
    # Calculate price_per_km because the model expects it
    if data.distance_km <= 0:
        price_per_km = 0
    else:
        price_per_km = data.price_asked / data.distance_km
        
    features = pd.DataFrame([{
        'dist_km': data.distance_km,
        'price': data.price_asked,
        'price_per_km': price_per_km
    }])
    
    is_scam = scam_model.predict(features)[0]
    probability = scam_model.predict_proba(features)[0][1]
    
    result = "SCAM" if is_scam == 1 else "FAIR"
    
    return {
        "verdict": result,
        "scam_probability": round(probability * 100, 1),
        "warning": "Price is abnormally high!" if is_scam == 1 else "Price looks reasonable."
    }

@app.get("/hotspots")
def get_hotspots():
    centers = hotspot_model.cluster_centers_
    hotspots = []
    for center in centers:
        hotspots.append({"lat": center[0], "lon": center[1]})
    return {"hotspots": hotspots}
