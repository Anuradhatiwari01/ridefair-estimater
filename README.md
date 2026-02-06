# RideFair – Auto Fare Estimator for Students

## Live Demo
🔗 https://ride-fair-estimater.vercel.app/

---

## Overview
RideFair is a web application that helps students estimate a fair auto-rickshaw fare before starting a ride.  
It provides an expected price range so students can avoid being overcharged.

---

## Why I Built This
In many college areas, auto-rickshaws do not use meters.  
Drivers often quote random prices, and students are unsure what is reasonable.

I built RideFair to help students make better fare decisions using distance, time, and past ride data.

---

## Key Features
- Enter pickup and drop location to get an estimated fare  
- Shows a safe price range instead of a single value  
- Warns if the quoted price is much higher than normal  
- Displays common student pickup areas on an interactive map  
- Simple and beginner-friendly interface  

---

## How It Works
The system estimates a normal fare based on:

- Distance between locations  
- Time of day  
- Weekday vs weekend patterns  

Using these inputs and historical ride data, it predicts what a fair fare should be.  
If a driver asks for a significantly higher amount, the app highlights it with a warning.

---

## Tech Stack
- **Frontend:** React.js  
- **Backend:** Python (FastAPI)  
- **Database:** MySQL  
- **Maps & UI:** Leaflet  

---

## Data Used
The project uses sample and collected ride data designed to reflect common student travel patterns.  
The main purpose was to learn full-stack development and basic fare prediction, not to build a production-ready system.

---

## What I Learned
- Designing and building backend APIs with FastAPI  
- Connecting frontend and backend in a complete application  
- Using real-world style data for basic prediction logic  
- Presenting results clearly through an interactive UI  

---

## Future Improvements
- Use more real-world ride data for better accuracy  
- Add user login and ride history tracking  
- Improve estimation support for multiple cities  
- Add more advanced ML-based pricing models  

---

Built as a learning project to solve a real student problem.
