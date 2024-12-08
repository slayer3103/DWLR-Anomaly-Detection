import os
import time
import logging
import pandas as pd
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Folder for processed output files (relative to script directory)
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'output')

# Simulated processing delay (in seconds)
CHECK_INTERVAL = 5

@app.route('/get-results', methods=['GET'])
def get_results():
    """Fetch the latest processed results from the output folder."""
    try:
        # Check if output folder exists
        if not os.path.exists(OUTPUT_FOLDER):
            logging.error("Output folder not found.")
            return jsonify({'error': 'Output folder not found. Please check the server setup.'}), 500

        # Get all CSV files in the folder
        files = [f for f in os.listdir(OUTPUT_FOLDER) if f.endswith('.csv')]
        if not files:
            return jsonify({'error': 'No results available yet. Please upload a file.'}), 404

        # Get the latest file based on modification time
        latest_file = max(
            [os.path.join(OUTPUT_FOLDER, f) for f in files],
            key=os.path.getmtime
        )

        # Read the latest file into a DataFrame
        try:
            df = pd.read_csv(latest_file)
        except pd.errors.EmptyDataError:
            logging.error(f"Empty or corrupted file: {latest_file}")
            return jsonify({'error': 'The latest CSV file is empty or corrupted.'}), 400
        except pd.errors.ParserError:
            logging.error(f"Parsing error in file: {latest_file}")
            return jsonify({'error': 'Error parsing the CSV file. Please check its format.'}), 400

        # Convert DataFrame to JSON
        result_data = df.to_dict(orient='records')
        return jsonify(result_data)

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=False)  # Run Flask on port 5001
