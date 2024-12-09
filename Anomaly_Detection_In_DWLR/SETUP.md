## Installation

1. **Download the root/main folder to your local machine**

2. **Install all the Dependencies with their correct versions mentioned in README.md**

3. **Move the downloaded folder to htdocs under XAMPP installation folder**

## Setup

1. **Open the Xampp control panel and start Apache, MySQL**

2. **Open admin page for MySQL from Xampp control panel and add database named dwlr.sql present under backend**
   
3. **Open command line/PowerShell and then navigate to the backend folder under the root folder of the project**

4. **Run the three scripts input.py, predictions.py and result_updater.py each on different windows/panels**

5. **Open the browser and enter the URL- http://localhost/Anomaly_Detection_In_DWLR/frontend/login.php (if you have downloaded the folder as it is)**

## Walkthrough

1. **Enter username=> admin and password=> admin in the login page**
2. **Click upload and then select the test_data.csv file or you can create your own CSV file using the data_generator_scripts folder under backend, In case you are creating your own CSV file remember that each city must have 31 rows atleast to create 1 row of result at the end also you need to remove the columns named time, month and anomaly before you use it as input**
3. **After successfully uploading the CSV file you will be redirected to the result page. Check the scripts running in the backend (input.py, prediction.py and result_updater.py) once there is a change in the state, refresh the result page and then dynamically choose the DWLR-ID and timestamp to get the result** 
   
