import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Parameters
num_rows = 15
initial_depth = 35.0  # Starting depth
max_depth = 66.0  # Max depth limit for dry conditions
min_depth_monsoon = 20.0  # Depth limit for monsoon
temp_min = 20.0  # Minimum groundwater temperature
temp_max = 26.0  # Maximum groundwater temperature
battery_life = 1000  # Battery life in readings
battery_replace_threshold = 0.1  # Threshold to replace battery

city_dwlr_ids = {
    "kaladera": "kaladera_01",
    "Mumbai": "mumbai_01",
    "Delhi": "delhi_01",
    "Bangalore": "DWLR004",
    "chennai": "chennai_01",
    "guwahati": "guwahati_01"}
    
city = "guwahati"  # Adjust this value to generate data for a specific city 
dwlr_id = city_dwlr_ids[city]


# Month ranges
seasonal_ranges = {
    'Jan': (35, 45),
    'Feb': (36, 47),
    'Mar': (40, 49),  # Pre-summer buffer
    'Apr': (45, 55),
    'May': (51, 63),
    'Jun': (52, 66),
    'Jul': (45, 55),
    'Aug': (30, 44),  # Pre-monsoon buffer
    'Sep': (20, 30),
    'Oct': (25, 35),
    'Nov': (30, 40),
    'Dec': (33, 43),
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
    'depth_sudden': 0.002  # New anomaly probability for sudden depth change
}

# Generate data
for i in range(num_rows):
    # Determine month and seasonal depth range
    month = current_date.strftime("%b")
    depth_min, depth_max = seasonal_ranges[month]
    prev_depth = depth  # Store previous depth for anomaly checks
    prev_battery_level = battery_level  # Store previous battery level for battery stuck anomaly

    # Adjust depth gradually within seasonal limits
    if depth >= depth_max - 0.5:  # If close to upper boundary, bounce down
        depth -= np.random.uniform(0.02, 0.1)
    elif depth <= depth_min + 0.5:  # If close to lower boundary, bounce up
        depth += np.random.uniform(0.02, 0.1)
    else:
        # Slight random variation around the current depth to prevent exact repeats
        depth += np.random.uniform(-0.05, 0.05)

    # Ensure depth remains within the seasonal limits
    depth = max(min(depth, depth_max), depth_min)

    # Adjust temperature gradually with minor fluctuation
    if temperature >= temp_max - 0.2:
        temperature -= np.random.uniform(0.01, 0.03)  # Bounce down if too close to max
    elif temperature <= temp_min + 0.2:
        temperature += np.random.uniform(0.01, 0.03)  # Bounce up if too close to min
    else:
        temperature += np.random.uniform(-0.02, 0.02)  # Minor fluctuation within range

    # Ensure temperature remains within the permissible range
    temperature = max(min(temperature, temp_max), temp_min)

    # Update battery level
    battery_level -= 100 / battery_life
    if battery_level < battery_replace_threshold:
        battery_level = 100.0  # Replace battery when threshold is hit

    # Anomaly Detection Flags
    is_anomaly = 'Normal'
    
    # Apply anomalies
    if np.random.rand() < anomaly_prob['battery_drain'] and battery_level > 10:
        battery_level -= np.random.uniform(2, 4)  # Sudden battery drain
        is_anomaly = 'Battery Drain Anomaly'
    elif round(battery_level, 4) == round(prev_battery_level, 4):
        is_anomaly = 'Battery Stuck Anomaly'

    if np.random.rand() < anomaly_prob['temperature_sudden']:
        # Ensure the sudden change is outside the -1 to 1 range
        sudden_change = np.random.choice([-1, 1]) * np.random.uniform(1.5, 2)
        temperature += sudden_change
        is_anomaly = 'Temperature Sudden Change Anomaly'

    # Check for depth anomalies
    if round(depth, 4) == round(prev_depth, 4):
        is_anomaly = 'Depth Stuck Anomaly'
    elif np.abs(depth - prev_depth) >= np.random.uniform(2, 3) and np.random.rand() < anomaly_prob['depth_sudden']:
        # Ensure the sudden change is outside the -1 to 1 range
        sudden_change = np.random.choice([-1, 1]) * np.random.uniform(1.01, 3)
        depth += sudden_change
        is_anomaly = 'Depth Sudden Change Anomaly'

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
df.to_csv('dwlrdata_guwahati.csv', index=False)
print("Data generation complete. Saved as 'dwlrdata_seasonal_with_anomalies_fixed_v3.csv'.")
