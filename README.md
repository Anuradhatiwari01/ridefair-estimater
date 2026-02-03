# RideFair – Auto Fare Estimator for Students

## What this project does
RideFair is a web application that helps students estimate a fair auto-rickshaw fare before starting a ride.  
It shows a price range so students can avoid being overcharged.

## Why I built this
In many college areas, auto-rickshaws do not use meters.  
Drivers often quote random prices, and students don’t know what is reasonable.  
I built this project to help students make better decisions using past fare data.

## Main features
- Enter pickup and drop location to get an estimated fare
- Shows a safe price range instead of a single value
- Warns if the quoted price is much higher than normal
- Displays common pickup areas on a map
- Simple and easy-to-use interface

## How the system works
The system looks at:
- distance between locations
- time of day
- weekday or weekend

Using this information and past ride data, it estimates what a normal fare should be.  
If a driver asks for a much higher price, the system shows a warning.

## Tech used
- Frontend: React.js
- Backend: Python (FastAPI)
- Database: MySQL
- Maps: Leaflet

## Data used
The project uses sample and collected ride data created to reflect common student travel patterns.  
The goal was to learn how data flows through a complete system, not to build a production app.

## What I learned
- How to design a simple backend API
- How frontend and backend communicate
- How data can be used to make basic predictions
- How to explain results clearly to users

## Future improvements
- Use more real-world data for better accuracy
- Add user login and ride history
- Improve fare estimation for different cities
