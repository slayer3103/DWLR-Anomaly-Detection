<?php
session_start(); // Start session

// Check if the form was submitted
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_FILES["csvFile"])) {
    $file = $_FILES["csvFile"]["tmp_name"]; // Get temporary file path
    $url = "http://127.0.0.1:5000/upload";  // Flask endpoint

    // Validate file
    if (!is_uploaded_file($file)) {
        echo "<script>alert('File upload failed. Please try again.');</script>";
        exit();
    }

    // Set up CURL to send the file
    $cfile = new CURLFile($file, 'text/csv', $_FILES["csvFile"]["name"]); // Positional arguments only
    $data = ['file' => $cfile];

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true); // Get response
    curl_setopt($ch, CURLOPT_TIMEOUT, 60);         // Set timeout

    $response = curl_exec($ch);                    // Execute CURL
    $http_status = curl_getinfo($ch, CURLINFO_HTTP_CODE); // Get status code
    curl_close($ch);

    // Handle response
    if ($http_status == 302 || $http_status == 200) { 
        // Redirect to result.html on success
        header("Location: result.html");
        exit();
    } else {
        // Show error if the upload fails
        echo "<script>alert('Error uploading the file to the server. HTTP Status: $http_status');</script>";
    }
}
?>





<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DWLR Dashboard</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <link rel="stylesheet" href="styles.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.7.0/chart.min.js"></script>
</head>

<body>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top shadow-sm">
        <a class="navbar-brand" href="#">DWLR Dashboard</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item">
                    <a class="nav-link active-link" href="login.php">Login</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link active-link" href="#home">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="notifications.html">Notifications</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="settings.html">Settings</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#contact">Contact Us</a>
                </li>
            </ul>
        </div>
    </nav>

    <div class="container-fluid mt-5 px-4">
        <!-- Home Section -->
        <div id="home" class="section text-center">
            <h1 class="section-title">Welcome to the DWLR Dashboard</h1>
            <p class="section-description">Monitor and visualize data from Digital Water Level Recorders (DWLRs) across the nation. Stay informed about water level trends, device statuses, and system alerts.</p>
        </div>
        <div class="banner">
            <img src="assets/hero3.jpg" class="img-fluid my-4" alt="Dashboard Overview">
        </div>
    </div>

    <div class="container mt-5 pt-5">
        <h2 class="text-center">Upload Processed CSV File</h2>
        <!-- CSV Upload Form -->
        <form method="POST" enctype="multipart/form-data" class="mb-4">
            <div class="form-group">
                <label for="csvFile">Select Processed CSV File:</label>
                <input type="file" name="csvFile" id="csvFile" accept=".csv" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Upload</button>
        </form>
    </div>

    <!-- Features Section -->
    <div class="mt-5">
        <h2 class="section-title text-center">Features</h2>
        <div class="row">
            <div class="col-md-4">
                <div class="feature-box text-center shadow">
                    <i class="fas fa-chart-line fa-3x mb-3"></i>
                    <h4>Fast Analysis of data</h4>
                    <p>Get instant updates on water level changes, device status, and potential issues.</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="feature-box text-center shadow">
                    <i class="fas fa-bell fa-3x mb-3"></i>
                    <h4>Alerts and Notifications</h4>
                    <p>Receive timely alerts for abnormalities, low battery levels, and data unavailability.</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="feature-box text-center shadow">
                    <i class="fas fa-cogs fa-3x mb-3"></i>
                    <h4>Customizable Settings</h4>
                    <p>Personalize your dashboard with various notification preferences and themes.</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
