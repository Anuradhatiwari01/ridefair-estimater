import axios from 'axios';

// This points to your running Python backend
const API_URL = 'https://ridefair-estimater.onrender.com/';

export const getFairPrice = async (distance, hour, isWeekend) => {
    const response = await axios.post(`${API_URL}/predict-price`, {
        distance_km: parseFloat(distance),
        hour: parseInt(hour),
        is_weekend: parseInt(isWeekend)
    });
    return response.data;
};

export const detectScam = async (distance, price) => {
    const response = await axios.post(`${API_URL}/detect-scam`, {
        distance_km: parseFloat(distance),
        price_asked: parseFloat(price)
    });
    return response.data;
};

export const getHotspots = async () => {
    const response = await axios.get(`${API_URL}/hotspots`);
    return response.data;
};
