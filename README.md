# RideFair: AI-Powered Auto Fare Estimator

### Introduction 
This is **RideFair**, a full-stack web application I built to solve a daily problem faced by students: **negotiating auto-rickshaw fares.**

###  The Real-World Problem
In many university towns, local auto-rickshaws do not use fixed meters. This leads to two major issues:
1.  **Overcharging:** Students often pay 2x or 3x the fair price because they don't know the standard rates.
2.  **Lack of Data:** There is no easy way to know if a quoted price is reasonable or a scam, especially during night hours or exams.

###  My Solution
I built an intelligent platform that acts as a "Fare Arbitrator." It doesn't just calculate distance; it uses **Machine Learning** to understand pricing patterns based on time, weekends, and historical data.

---

### Tech Stack
I designed this as a modern **Microservice Architecture**:
* **Frontend:** React.js (Vite) + Leaflet Maps for the interactive dashboard.
* **Backend:** Python FastAPI (chosen for high performance and async capabilities).
* **Database:** MySQL (utilized `Spatial Data Types` for efficient geospatial queries).
* **Machine Learning:** Scikit-Learn (trained on synthetic city data).

---

###  How the AI Works (The Core Logic)
I integrated **three specific algorithms** to solve different parts of the problem:

#### 1. Price Prediction (Linear Regression)
* **Goal:** Calculate the "Fair Price."
* **Logic:** The model analyzes the relationship between **Distance**, **Time of Day** (Peak vs. Non-Peak), and **Day Type** (Weekend vs. Weekday) to predict a fair fare.

#### 2. Scam Detection (Logistic Regression)
* **Goal:** Warn users if they are being cheated.
* **Logic:** This is a classification model. It looks at the `Price Per Km` and flags any ride as a **"SCAM"** or **"SAFE"** based on dynamic probability thresholds.

#### 3. Hotspot Mapping (K-Means Clustering)
* **Goal:** Show students where to find rides.
* **Logic:** I used unsupervised learning to cluster historical pickup locations. The map visualizes these "Centroids" (Hotspots) so users know the best place to catch an auto.

---

###  Key Features
* **Interactive Map:** Visualizes high-demand zones using AI clustering.
* **Real-Time Estimation:** Get a price range instantly before talking to a driver.
* **Scam Alert System:** Red/Green indicators tell you immediately if a price is too high.
* **System Architecture:** Decoupled Frontend and Backend communicating via REST APIs.

---

###  Future Improvements
* **Crowdsourcing:** Allowing users to submit their real ride data to retrain the models automatically.
* **Google Maps API:** Upgrading from Haversine distance to real-time road traffic analysis.

---
