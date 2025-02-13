# Air Quality Prediction (PM10)

## 📌 Project Overview 

This project focuses on predicting PM10 air pollution levels using time-series forecasting techniques. The dataset consists of air quality measurements over time, with features such as temperature, pressure, wind speed, and precipitation. The primary goal is to develop an accurate predictive model using machine learning and deep learning techniques, particularly LSTM-based neural networks.

## 🚀 Features

- Data preprocessing and cleaning

- Machine learning model (LSTM) for PM10 prediction

- Visualization of air quality trends

- Performance evaluation metrics


## 📂 Dataset 
The dataset contains historical air quality data, including PM10 levels and relevant meteorological parameters.
It's split into 3 files for training, validation, and testing purposes.
The dataset is available in the ```data``` folder.


## 🐋 Running the API with Docker
###  Build the Docker Image  
Run the following command in the project root directory to build the Docker image:  
```sh
docker build -t airqualityprediction .
```
###  Run the Docker Container
After building the image, start a container using:
```sh
docker run -p 8000:8000 airqualityprediction
```

## 🛠️ Usage
To use the API for PM10 prediction, send a ```POST``` request to the ```/predict``` endpoint with a JSON payload containing air quality parameters.

### 📤 Example Request
**Request URL:** 
```bash
http://localhost:8000/predict
```
**Headers**:
```json
{
  "Content-Type": "application/json"
}
```
**Sample JSON Payload (from ```test_data``` folder):**
```json
{
  "datetime": "2024-09-12 20:00:00",
  "temperature": 10.0,
  "rain": 3.9,
  "pressure": 1009.0,
  "precipitation": 96.0,
  "wind_speed": 10.0,
  "clouds": "oblačno",
  "PM10": 45.2
}
```

### 📥 Example Response

**If the request is successful, the API will return a predicted PM10 value:**

```json
{
    "prediction": [
        2.386687755584717
    ]
}
```

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Feel free to contribute! Open an issue or submit a pull request if you have improvements or suggestions.