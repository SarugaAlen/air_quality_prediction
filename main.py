from datetime import datetime
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from utils.slidding_window import slidding_window

app = FastAPI()


class TimeSeriesModel(BaseModel):
    datetime: str
    PM10: float
    temperature: float
    rain: float
    pressure: float
    precipitation: float
    wind_speed: float
    clouds: str


minmax_columns = ['rain', 'precipitation', 'pressure_wind_interaction']
standard_columns = ['PM10', 'temperature', 'pressure', 'wind_speed']

minmax_scaler = joblib.load("models/scaler_minmax.pkl")
standard_scaler = joblib.load("models/scaler_standard.pkl")
scaler = joblib.load("models/scaler.pkl")
model = load_model("models/best_lstm_model.h5")
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae', 'mse'])


@app.get("/")
async def root():
    return {"message": "Air Quality Prediction API",
            "timestamp": datetime.now()}


@app.post("/predict/")
async def predict(data: List[TimeSeriesModel]):
    try:
        df = pd.DataFrame([item.dict() for item in data])
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.sort_values('datetime', inplace=True)

        df = pd.get_dummies(df, columns=['clouds'])
        df['month'] = df['datetime'].dt.month
        df['day_of_week'] = df['datetime'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
        df['pressure_wind_interaction'] = df['pressure'] * df['wind_speed']

        df['rain'] = np.log1p(df['rain'])
        df['wind_speed'] = np.log1p(df['wind_speed'])

        minmax_scaler.fit(df[minmax_columns])
        standard_scaler.fit(df[standard_columns])

        data = df['PM10']
        data = data.values.reshape(-1, 1)
        data_scaled = scaler.transform(data)

        X, _ = slidding_window(data_scaled, window_size=48)

        X = X.reshape(X.shape[0], 1, X.shape[1])

        prediction = model.predict(X)

        prediction = scaler.inverse_transform(prediction)

        prediction = prediction.flatten().tolist()

        return {
            "prediction": prediction
        }

    except Exception as e:
        return {"error": str(e)}
