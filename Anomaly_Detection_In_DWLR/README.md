# DWLR Anomaly Detection System

## Overview

The **Digital Water Level Recorder (DWLR) Anomaly Detection System** is a comprehensive solution designed to monitor groundwater levels, temperature, and battery status using advanced machine learning techniques. This project provides real-time anomaly detection and visualization through a user-friendly dashboard, helping stakeholders ensure efficient water resource management.

---

## Features

- **Data Processing & Analysis**: Processes water level, temperature, and battery data for multiple locations.
- **Anomaly Detection**: Utilizes LSTM models for real-time detection of anomalies such as sudden changes or stuck values.
- **User-Friendly Dashboard**: Interactive web-based dashboard to upload data, view results, and analyze anomalies.
- **City-Specific Customization**: Thresholds and models tailored for various cities (e.g., Chennai, Guwahati, Kaladera, Srinagar).
- **Scalable & Modular**: Designed to be extensible for additional locations and features.

---

## Technologies Used

- **Python**: Backend processing, anomaly detection, and APIs.
- **Flask**: Backend API for handling data uploads and processing.
- **Watchdog**: Monitors the uploads folder for new data files.
- **TensorFlow/Keras**: LSTM models for training and detecting anomalies.
- **PHP**: Backend for user authentication and file uploads.
- **HTML/CSS/JavaScript**: Frontend dashboard and interactivity.
- **Bootstrap**: Responsive design for the dashboard.
- **XAMPP**: Local server for hosting the web application.
- **MySQL**: User authentication database.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/slayer/DWLR-Anomaly-Detection.git
   cd DWLR-Anomaly-Detection
