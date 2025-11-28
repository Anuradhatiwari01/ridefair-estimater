import pandas as pd
import numpy as np
import pickle
import random
import mysql.connector
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.cluster import KMeans

print(" Starting AI Engine Build...")

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',       
    'password': '2401', 
    'database': 'ride_estimator'
}

# GENERATE REALISTIC MOCK DATA
print("Generating 2,000 synthetic ride records...")

data = []
zones = [
    {"lat": 28.54, "lon": 77.33}, # College
    {"lat": 28.58, "lon": 77.38}, # Mall
    {"lat": 28.62, "lon": 77.29}  # Metro Station
]

for _ in range(2000):-
    zone = random.choice(zones)
    lat = zone["lat"] + random.uniform(-0.01, 0.01)
    lon = zone["lon"] + random.uniform(-0.01, 0.01)
    
    # Features (Linear Regression) 
    dist_km = round(random.uniform(1.0, 15.0), 2)
    hour = random.randint(6, 22) # 6 AM to 10 PM
    is_weekend = random.choice([0, 1])
    
    is_peak = 1 if (8 <= hour <= 10) or (17 <= hour <= 20) else 0
    
    fair_price = 25 + (dist_km * 12)
    
    if is_peak: fair_price *= 1.4 
    if is_weekend: fair_price += 20 
    
    # Scam Logic (Logistic Regression)
    is_scam = 0
    price_paid = fair_price
    
    if random.random() < 0.15:
        is_scam = 1
        price_paid = fair_price * random.uniform(1.8, 3.0)
    else:
        price_paid += random.uniform(-10, 10)
        
    data.append([lat, lon, dist_km, hour, is_weekend, round(price_paid), is_scam])

# Convert to DataFrame
df = pd.DataFrame(data, columns=['lat', 'lon', 'dist_km', 'hour', 'is_weekend', 'price', 'is_scam'])

# TRAIN THE 3 MODELS

# Linear Regression (Predict Fair Price) 
print("Training Linear Regression (Price Estimator)...")
X_price = df[['dist_km', 'hour', 'is_weekend']]
y_price = df['price']
lin_reg = LinearRegression()
lin_reg.fit(X_price, y_price)

# Logistic Regression (Scam Detector) 
print("Training Logistic Regression (Scam Detector)...")
# Added a feature: 'price_per_km' because scammers usually have high rates
df['price_per_km'] = df['price'] / df['dist_km']
X_scam = df[['dist_km', 'price', 'price_per_km']]
y_scam = df['is_scam']
log_reg = LogisticRegression()
log_reg.fit(X_scam, y_scam)

# K-Means (Hotspot Identification) 
print("Training K-Means (Hotspot Finder)...")
X_loc = df[['lat', 'lon']]
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X_loc)

# SAVE TO FILE (.pkl)

print("Saving models to 'all_models.pkl'...")
models = {
    "price_model": lin_reg,
    "scam_model": log_reg,
    "hotspot_model": kmeans
}
with open("all_models.pkl", "wb") as f:
    pickle.dump(models, f)

try:
    print("Connecting to MySQL to seed data...")
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Insert first 100 rows just to have some data in DB
    count = 0
    for row in data[:100]: 
        sql = """
        INSERT INTO ride_data 
        (pickup_loc, distance_km, hour_of_day, is_weekend, price_paid, is_scam)
        VALUES (ST_GeomFromText('POINT(%s %s)', 4326), %s, %s, %s, %s, %s)
        """
        val = (row[1], row[0], row[2], row[3], row[4], row[5], row[6])
        cursor.execute(sql, val)
        count += 1
        
    conn.commit()
    print(f"Successfully inserted {count} rows into MySQL!")
    cursor.close()
    conn.close()

except Exception as e:
    print(f"Database skipped or failed: {e}")
    print("Continuing... (Models are still saved)")
