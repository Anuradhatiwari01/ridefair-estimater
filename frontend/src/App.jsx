import { useState, useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import { getFairPrice, detectScam, getHotspots } from './api'
import './App.css'

function App() {
  // State for K-Means (Map)
  const [hotspots, setHotspots] = useState([])

  // State for Linear Regression (Price Predictor)
  const [priceInputs, setPriceInputs] = useState({ dist: 5, hour: 10, weekend: 0 })
  const [priceResult, setPriceResult] = useState(null)

  // State for Logistic Regression (Scam Detector)
  const [scamInputs, setScamInputs] = useState({ dist: 5, price: 100 })
  const [scamResult, setScamResult] = useState(null)

  // Load Hotspots on Startup
  useEffect(() => {
    async function loadHotspots() {
      try {
        const data = await getHotspots()
        setHotspots(data.hotspots)
      } catch (e) {
        console.error("Failed to connect to API")
      }
    }
    loadHotspots()
  }, [])

  // Handlers
  const handlePredictPrice = async () => {
    const data = await getFairPrice(priceInputs.dist, priceInputs.hour, priceInputs.weekend)
    setPriceResult(data)
  }

  const handleDetectScam = async () => {
    const data = await detectScam(scamInputs.dist, scamInputs.price)
    setScamResult(data)
  }

  return (
    <div className="container">
      <h1>🚖 RideFair: AI Fare Estimator</h1>
      
      {/* SECTION 1: K-MEANS CLUSTERING VISUALIZATION */}
      <div className="card">
        <h3>📍 High Demand Zones (AI Clusters)</h3>
        <p><i>Powered by K-Means Algorithm</i></p>
        <div style={{ height: '300px', width: '100%' }}>
          {/* Centered on approx location */}
          <MapContainer center={[28.58, 77.33]} zoom={12} style={{ height: '100%', width: '100%' }}>
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {hotspots.map((pt, idx) => (
              <Marker key={idx} position={[pt.lat, pt.lon]}>
                <Popup>🔥 Hotspot Zone {idx + 1}</Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
        
        {/* SECTION 2: LINEAR REGRESSION */}
        <div className="card" style={{ flex: 1 }}>
          <h3>💰 Fair Price Predictor</h3>
          <p><i>Algorithm: Linear Regression</i></p>
          
          <label>Distance (km):</label>
          <input type="number" value={priceInputs.dist} 
            onChange={e => setPriceInputs({...priceInputs, dist: e.target.value})} />
          
          <br />
          <label>Hour (0-23):</label>
          <input type="number" value={priceInputs.hour} 
            onChange={e => setPriceInputs({...priceInputs, hour: e.target.value})} />
            
          <br />
          <label>Weekend?</label>
          <select onChange={e => setPriceInputs({...priceInputs, weekend: e.target.value})}>
            <option value="0">No</option>
            <option value="1">Yes</option>
          </select>

          <br />
          <button onClick={handlePredictPrice}>Predict Fare</button>

          {priceResult && (
            <div style={{ marginTop: '15px', padding: '10px', background: '#e3f2fd' }}>
              <h2>₹{priceResult.fair_price}</h2>
              <small>{priceResult.message}</small>
            </div>
          )}
        </div>

        {/* SECTION 3: LOGISTIC REGRESSION */}
        <div className="card" style={{ flex: 1 }}>
          <h3>🚨 Scam Detector</h3>
          <p><i>Algorithm: Logistic Regression</i></p>
          
          <label>Distance (km):</label>
          <input type="number" value={scamInputs.dist} 
            onChange={e => setScamInputs({...scamInputs, dist: e.target.value})} />
          
          <br />
          <label>Price Asked (₹):</label>
          <input type="number" value={scamInputs.price} 
            onChange={e => setScamInputs({...scamInputs, price: e.target.value})} />
            
          <br />
          <button onClick={handleDetectScam} style={{backgroundColor: '#dc3545'}}>Check for Scam</button>

          {scamResult && (
            <div style={{ marginTop: '15px', padding: '10px', border: '1px solid #ccc' }}>
              <h2 className={scamResult.verdict === "SCAM" ? "scam" : "safe"}>
                {scamResult.verdict}
              </h2>
              <p>Probability: {scamResult.scam_probability}%</p>
              <small>{scamResult.warning}</small>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App