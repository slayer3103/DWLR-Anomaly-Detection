import os
import pandas as pd
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


# ==============================
# City-Specific Models and Paths
# ==============================

# Base directory of the project (parent of the backend folder)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define directories relative to BASE_DIR
MODEL_DIR = os.path.join(BASE_DIR, '/trained_models')  
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'output')

city_models = {
    "chennai": {
        "depth_model": os.path.join(MODEL_DIR, "depth_model_chennai.h5"),
        "temperature_model": os.path.join(MODEL_DIR, "temperature_model_chennai.h5"),
        "battery_model":  os.path.join(MODEL_DIR,"battery_model_chennai.h5"),
        "scaler_dict":  os.path.join(MODEL_DIR,"scalers_chennai.pkl"),
    },
        "guwahati": {
        "depth_model":  os.path.join(MODEL_DIR,"depth_model_guwahati.h5"),
        "temperature_model": os.path.join(MODEL_DIR,"temperature_model_guwahati.h5"),
        "battery_model":  os.path.join(MODEL_DIR,"battery_model_guwahati.h5"),
        "scaler_dict": os.path.join(MODEL_DIR,"scalers_guwahati.pkl"),
    },
    "kaladera": {
        "depth_model":  os.path.join(MODEL_DIR,"depth_model_kaladera.h5"),
        "temperature_model":  os.path.join(MODEL_DIR,"temperature_model_kaladera.h5"),
        "battery_model":  os.path.join(MODEL_DIR,"battery_model_kaladera.h5"),
        "scaler_dict":  os.path.join(MODEL_DIR,"scalers_kaladera.pkl"),
    },
    "srinagar": {
        "depth_model":  os.path.join(MODEL_DIR,"depth_model_srinagar.h5"),
        "temperature_model":  os.path.join(MODEL_DIR,"temperature_model_srinagar.h5"),
        "battery_model":  os.path.join(MODEL_DIR,"battery_model_srinagar.h5"),
        "scaler_dict": os.path.join(MODEL_DIR,"scalers_srinagar.pkl"),
    },# Add other cities similarly...
}

# Ensure folders exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Load city-specific models and scalers
models = {}
scalers = {}

for city, paths in city_models.items():
    try:
        models[city] = {
            "depth_model": load_model(paths["depth_model"]),
            "temperature_model": load_model(paths["temperature_model"]),
            "battery_model": load_model(paths["battery_model"]),
        }
        with open(paths["scaler_dict"], "rb") as f:
            scalers[city] = pickle.load(f)
            print(f"Loaded models and scalers for {city}")
    except Exception as e:
        print(f"Error loading models or scalers for {city}: {e}")
        models[city] = None
        scalers[city] = None
 
# ==============================
# Anomaly Detection Logic with Automated Threshold Adjustment
# ==============================

def calculate_dynamic_threshold(reconstruction_losses, percentile=95):
    """Calculate threshold dynamically based on percentile."""
    return np.percentile(reconstruction_losses, percentile)

def detect_anomalies(model, sequences, percentile=95):
    """
    Detect anomalies by calculating reconstruction losses
    and using a dynamic threshold based on the percentile.
    """
    predictions = model.predict(sequences)
    reconstruction_losses = np.mean(np.abs(predictions - sequences), axis=(1, 2))
    threshold = calculate_dynamic_threshold(reconstruction_losses, percentile)
    return reconstruction_losses > threshold, reconstruction_losses, threshold

def process_city_data(city, city_df, sequence_length, percentiles):
    city_models_dict = models[city]
    city_scalers_dict = scalers[city]

    if city_models_dict is None or city_scalers_dict is None:
        print(f"Skipping city {city} due to missing models or scalers.")
        return None

    # Scale features
    try:
        depth_scaled = city_scalers_dict['Depth'].transform(city_df[['Depth']])
        temperature_scaled = city_scalers_dict['Temperature'].transform(city_df[['Temperature']])
        battery_scaled = city_scalers_dict['Battery Level'].transform(city_df[['Battery Level']])
    except Exception as e:
        print(f"Error scaling features for city {city}: {e}")
        return None

    # Create sequences
    def create_sequences(data, time_steps):
        sequences = []
        for i in range(len(data) - time_steps + 1):  # Corrected sequence generation
            sequences.append(data[i:i + time_steps])
        return np.array(sequences)

    depth_sequences = create_sequences(depth_scaled, sequence_length)
    temperature_sequences = create_sequences(temperature_scaled, sequence_length)
    battery_sequences = create_sequences(battery_scaled, sequence_length)

    if not depth_sequences.size or not temperature_sequences.size or not battery_sequences.size:
        print(f"Not enough data for LSTM sequences in city {city}.")
        return None

    # Detect anomalies dynamically
    depth_anomalies, depth_losses, depth_threshold = detect_anomalies(
        city_models_dict['depth_model'], depth_sequences, percentiles['Depth']
    )
    temperature_anomalies, temperature_losses, temp_threshold = detect_anomalies(
        city_models_dict['temperature_model'], temperature_sequences, percentiles['Temperature']
    )
    battery_anomalies, battery_losses, battery_threshold = detect_anomalies(
        city_models_dict['battery_model'], battery_sequences, percentiles['Battery Level']
    )

    # Adjust DataFrame
    adjusted_length = len(city_df) - sequence_length + 1
    adjusted_df = city_df.iloc[-adjusted_length:].reset_index(drop=True)  # Align to match prediction length
    adjusted_df['Depth_Anomaly'] = depth_anomalies
    adjusted_df['Temperature_Anomaly'] = temperature_anomalies
    adjusted_df['Battery_Anomaly'] = battery_anomalies
    adjusted_df['Anomaly'] = adjusted_df[['Depth_Anomaly', 'Temperature_Anomaly', 'Battery_Anomaly']].max(axis=1)

    # Log thresholds for debugging
    print(f"City: {city}, Depth Threshold: {depth_threshold}, Temperature Threshold: {temp_threshold}, Battery Threshold: {battery_threshold}")

    return adjusted_df


def predict_anomalies(file_path, sequence_length, percentiles):
    df = pd.read_csv(file_path)
    print(f"Processing file: {file_path}")

    # Ensure required columns are present
    required_columns = ['Timestamp', 'Depth', 'Temperature', 'Battery Level', 'DWLR_ID']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Missing required columns in the input file: {file_path}")

    # Derive city from DWLR_ID
    df['City'] = df['DWLR_ID'].str.split('_').str[0]

    # Process each city
    results = []
    for city, city_df in df.groupby('City'):
        print(f"Processing data for city: {city}")
        if city not in city_models:
            print(f"Unknown city {city}, skipping...")
            continue

        processed_data = process_city_data(city, city_df, sequence_length, percentiles)
        if processed_data is not None:
            results.append(processed_data)

    return pd.concat(results, ignore_index=True) if results else None

# ==============================
# File Monitoring Logic
# ==============================
class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            try:
                percentiles = {
                    'Depth': 97,  # Adjust sensitivity by percentile
                    'Temperature': 97,
                    'Battery Level': 99
                }
                sequence_length = 30
                predictions = predict_anomalies(event.src_path, sequence_length, percentiles)
                if predictions is not None and not predictions.empty:
                    output_path = event.src_path.replace("uploads", "output").replace(".csv", "_predictions.csv")
                    predictions.to_csv(output_path, index=False)
                    print(f"Predictions saved to {output_path}")
                else:
                    print(f"No predictions generated for file: {event.src_path}")
            except Exception as e:
                print(f"Error processing file {event.src_path}: {e}")

if __name__ == "__main__":
    # Set up the event handler and observer
    event_handler = FileHandler()
    observer = Observer()

    try:
        observer.schedule(event_handler, UPLOAD_FOLDER, recursive=False)
        print(f"Monitoring folder: {UPLOAD_FOLDER}")
        observer.start()
    except FileNotFoundError as e:
        print(f"Error: {UPLOAD_FOLDER} does not exist. Please check your folder structure.")
        raise e

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
