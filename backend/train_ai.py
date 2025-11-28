import pandas as pd
import numpy as np
import pickle
import random
import mysql.connector
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.cluster import KMeans

print("⚙️  Starting AI Engine Build...")

# ==========================================
# 1. CONFIGURATION (UPDATE THIS!)
# ==========================================
# If you want to save this data to your MySQL DB, fill this in.
# If not, leave as is, the script will skip DB insertion if connection fails.
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',        # CHANGE THIS
    'password': '2401', # CHANGE THIS to your MySQL password
    'database': 'ride_estimator'
}

# ==========================================
# 2. GENERATE REALISTIC MOCK DATA
# ==========================================
print("📊 Generating 2,000 synthetic ride records...")

data = []
# Lat/Lon centers for Sitare University area (approx)
# We create 3 "Hotspots" (Clusters)
zones = [
    {"lat": 28.54, "lon": 77.33}, # College
    {"lat": 28.58, "lon": 77.38}, # Mall
    {"lat": 28.62, "lon": 77.29}  # Metro Station
]

for _ in range(2000):
    # -- Location (K-Means) --
    zone = random.choice(zones)
    # Add random noise so points aren't all exactly on top of each other
    lat = zone["lat"] + random.uniform(-0.01, 0.01)
    lon = zone["lon"] + random.uniform(-0.01, 0.01)
    
    # -- Features (Linear Regression) --
    dist_km = round(random.uniform(1.0, 15.0), 2)
    hour = random.randint(6, 22) # 6 AM to 10 PM
    is_weekend = random.choice([0, 1])
    
    # Logic: Peak hours are 8-10 AM and 5-8 PM
    is_peak = 1 if (8 <= hour <= 10) or (17 <= hour <= 20) else 0
    
    # -- Pricing Logic --
    # Formula: Base ₹25 + (₹12 * km)
    fair_price = 25 + (dist_km * 12)
    
    if is_peak: fair_price *= 1.4  # 40% hike in peak
    if is_weekend: fair_price += 20 # Flat extra on weekend
    
    # -- Scam Logic (Logistic Regression) --
    is_scam = 0
    price_paid = fair_price
    
    # 15% chance of a scam (Driver asks for double)
    if random.random() < 0.15:
        is_scam = 1
        price_paid = fair_price * random.uniform(1.8, 3.0)
    else:
        # Normal negotiation variance (+/- ₹10)
        price_paid += random.uniform(-10, 10)
        
    data.append([lat, lon, dist_km, hour, is_weekend, round(price_paid), is_scam])

# Convert to DataFrame
df = pd.DataFrame(data, columns=['lat', 'lon', 'dist_km', 'hour', 'is_weekend', 'price', 'is_scam'])

# ==========================================
# 3. TRAIN THE 3 MODELS
# ==========================================

# --- A. Linear Regression (Predict Fair Price) ---
print("🧠 Training Linear Regression (Price Estimator)...")
X_price = df[['dist_km', 'hour', 'is_weekend']]
y_price = df['price']
lin_reg = LinearRegression()
lin_reg.fit(X_price, y_price)

# --- B. Logistic Regression (Scam Detector) ---
print("🧠 Training Logistic Regression (Scam Detector)...")
# We add a feature: 'price_per_km' because scammers usually have high rates
df['price_per_km'] = df['price'] / df['dist_km']
X_scam = df[['dist_km', 'price', 'price_per_km']]
y_scam = df['is_scam']
log_reg = LogisticRegression()
log_reg.fit(X_scam, y_scam)

# --- C. K-Means (Hotspot Identification) ---
print("🧠 Training K-Means (Hotspot Finder)...")
X_loc = df[['lat', 'lon']]
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X_loc)

# ==========================================
# 4. SAVE TO FILE (.pkl)
# ==========================================
print("💾 Saving models to 'all_models.pkl'...")
models = {
    "price_model": lin_reg,
    "scam_model": log_reg,
    "hotspot_model": kmeans
}
with open("all_models.pkl", "wb") as f:
    pickle.dump(models, f)

# ==========================================
# 5. SYNC WITH DATABASE (OPTIONAL)
# ==========================================
try:
    print("🔌 Connecting to MySQL to seed data...")
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Insert first 100 rows just to have some data in DB
    count = 0
    for row in data[:100]: 
        # row = [lat, lon, dist, hour, weekend, price, scam]
        sql = """
        INSERT INTO ride_data 
        (pickup_loc, distance_km, hour_of_day, is_weekend, price_paid, is_scam)
        VALUES (ST_GeomFromText('POINT(%s %s)', 4326), %s, %s, %s, %s, %s)
        """
        # Note: MySQL POINT is (Longitude, Latitude) -> (row[1], row[0])
        val = (row[1], row[0], row[2], row[3], row[4], row[5], row[6])
        cursor.execute(sql, val)
        count += 1
        
    conn.commit()
    print(f"✅ Successfully inserted {count} rows into MySQL!")
    cursor.close()
    conn.close()

except Exception as e:
    print(f"⚠️  Database skipped or failed: {e}")
    print("Continuing... (Models are still saved)")

print("\n🚀 SUCCESS! Step 3 Complete. Ready for API.")