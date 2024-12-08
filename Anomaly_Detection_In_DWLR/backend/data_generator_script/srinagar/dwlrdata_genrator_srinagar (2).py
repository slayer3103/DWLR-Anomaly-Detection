import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Parameters
num_rows = 15
initial_depth = 20.0  # Starting depth for Srinagar
max_depth_summer = 55.0  # Maximum depth during peak dry months
min_depth_monsoon = 10.0  # Depth limit during monsoon recharge
temp_min = 14.0  # Minimum groundwater temperature for Srinagar's winter
temp_max = 20.0  # Maximum groundwater temperature for Srinagar's summer
battery_life = 1000  # Battery life in readings
battery_replace_threshold = 0.1  # Threshold to replace battery

city_dwlr_ids = {
    "kaladera": "kaladera_01",
    "Mumbai": "mumbai_01",
    "srinagar": "srinagari_01",
    "Bangalore": "DWLR004",
    "chennai": "chennai_01",
    "guwahati": "guwahati_01"}
    
city = "srinagar"  # Adjust this value to generate data for a specific city 
dwlr_id = city_dwlr_ids[city]


# Month ranges
seasonal_ranges = {
    'Jan': (35, 45),   # Winter
    'Feb': (33, 43),   # Winter
    'Mar': (30, 40),   # Pre-summer
    'Apr': (25, 35),   # Pre-summer
    'May': (20, 30),   # Summer start
    'Jun': (18, 25),   # Peak summer
    'Jul': (15, 20),   # Monsoon recharge
    'Aug': (10, 20),   # Peak monsoon recharge
    'Sep': (12, 22),   # Post-monsoon
    'Oct': (25, 35),   # Autumn
    'Nov': (30, 40),   # Early winter
    'Dec': (32, 42),   # Winter
}

# Initialize data lists
data = []
current_date = datetime(2024, 1, 1)
depth = initial_depth
temperature = np.random.uniform(temp_min, temp_max)
battery_level = 100.0
reading_count = 0

# Anomaly probabilities
anomaly_prob = {
    'battery_drain': 0.001,
    'battery_stuck': 0.001,
    'temperature_sudden': 0.002,
    'depth_stuck': 0.003,
    'depth_sudden': 0.002  # New anomaly for sudden depth change
}

# Generate data
for i in range(num_rows):
    # Determine month and seasonal depth range
    month = current_date.strftime("%b")
    depth_min, depth_max = seasonal_ranges[month]

    # Adjust depth gradually within seasonal limits, avoiding repeat values
    if depth >= depth_max - 0.5:  # If close to upper boundary, bounce down
        depth -= np.random.uniform(0.1, 0.2)
    elif depth <= depth_min + 0.5:  # If close to lower boundary, bounce up
        depth += np.random.uniform(0.1, 0.2)
    else:
        # Slight random variation around the current depth
        depth += np.random.uniform(-0.05, 0.05)

    # Enforce seasonal depth limits
    depth = max(min(depth, depth_max), depth_min)

    # Adjust groundwater temperature gradually with minor fluctuation
    if temperature >= temp_max - 0.2:
        temperature -= np.random.uniform(0.01, 0.03)
    elif temperature <= temp_min + 0.2:
        temperature += np.random.uniform(0.01, 0.03)
    else:
        temperature += np.random.uniform(-0.02, 0.02)

    # Ensure temperature remains within permissible range
    temperature = max(min(temperature, temp_max), temp_min)

    # Update battery level
    battery_level -= 100 / battery_life
    if battery_level < battery_replace_threshold:
        battery_level = 100.0  # Replace battery when threshold is hit

    # Anomaly Detection Flags
    is_anomaly = 'Normal'
    
    # Apply anomalies based on probabilities
    if np.random.rand() < anomaly_prob['battery_drain'] and battery_level > 10:
        battery_level -= np.random.uniform(2, 4)  # Sudden battery drain
        is_anomaly = 'Battery Drain Anomaly'
    elif np.random.rand() < anomaly_prob['battery_stuck']:
        battery_level = battery_level  # Battery level stuck anomaly
        is_anomaly = 'Battery Stuck Anomaly'

    # Sudden temperature change anomaly
    if np.random.rand() < anomaly_prob['temperature_sudden']:
        temp_change = np.random.uniform(-2, 2)
        if abs(temp_change) > 1:  # Ensure change is notable
            temperature += temp_change
            is_anomaly = 'Temperature Sudden Change Anomaly'
    
    # Depth sudden change anomaly
    if np.random.rand() < anomaly_prob['depth_sudden']:
        depth_change = np.random.uniform(-3, 3)
        if abs(depth_change) > 1:  # Ensure change is notable
            depth += depth_change
            is_anomaly = 'Depth Sudden Change Anomaly'

    # Depth stuck anomaly - exact match to previous depth value
    if len(data) > 0 and round(depth, 4) == round(data[-1]['Depth'], 4):
        is_anomaly = 'Depth Stuck Anomaly'
    
    # Battery stuck anomaly - exact match to previous battery level
    if len(data) > 0 and round(battery_level, 2) == round(data[-1]['Battery Level'], 2):
        is_anomaly = 'Battery Stuck Anomaly'

    # Append data to list
    data.append({
        'DWLR_ID': dwlr_id,
        'Timestamp': current_date.strftime('%d-%m-%Y %H:%M'),
        'Time': current_date.strftime('%H:%M:%S'),
        'Month': month,
        'Depth': round(depth, 4),
        'Temperature': round(temperature, 4),
        'Battery Level': round(battery_level, 2),
        'Anomaly': is_anomaly
    })
    # Move to next time step
    current_date += timedelta(hours=6)
    reading_count += 1

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('dwlrdata_srinagar_final.csv', index=False)
print("Data generation complete. Saved as 'dwlrdata_srinagar.csv'.")
