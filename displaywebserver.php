<?php
error_reporting(E_ALL);
ini_set('display_errors', '1');

$xml_arr = '';

if (file_exists('sensorData.xml')) {
    $xml_arr = simplexml_load_file('sensorData.xml');

    // Total number of timestamps recorded
    $total_timestamps = count($xml_arr->record);

    
    
    

    // Start the HTML table with CSS styling
    echo '<style>';
    echo 'body {';
    echo '    font-family: Arial, sans-serif;';
    echo '    background-color: #f4f4f4;';
    echo '}';
    echo 'h2 {';
    echo '    color: #333;';
    echo '}';
    echo 'table {';
    echo '    width: 100%;';
    echo '    border-collapse: collapse;';
    echo '    margin-bottom: 20px;';
    echo '}';
    echo 'th, td {';
    echo '    padding: 10px;';
    echo '    text-align: left;';
    echo '    border-bottom: 1px solid #ddd;';
    echo '}';
    echo 'th {';
    echo '    background-color: #f2f2f2;';
    echo '}';
    echo '.info {';
    echo '    background-color: #fff;';
    echo '    padding: 20px;';
    echo '    border-radius: 5px;';
    echo '    box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.1);';
    echo '}';
    echo '</style>';

    // Function to create a table for data
    function createTable($data, $title)
    {
        if (count($data) > 0) {
            echo "<h2>$title</h2>";
            echo '<table>';
            echo '<tr>';
            echo '<th>Timestamp</th>';
            echo '<th>Temperature (&deg;C)</th>';
            echo '<th>Humidity (%)</th>';
            echo '<th>Condition</th>';
            echo '</tr>';
            foreach ($data as $row) {
                echo '<tr>';
                echo '<td>' . $row['timestamp'] . '</td>';
                echo '<td>' . $row['temperature'] . '</td>';
                echo '<td>' . $row['humidity'] . '</td>';
                echo '<td>' . $row['condition'] . '</td>';
                echo '</tr>';
            }
            echo '</table>';
        } else {
            echo "<p>No data for $title</p>";
        }
    }

    // Initialize arrays to hold data
    $above_threshold_data = [];
    $collision_data = [];
    $high_wind_data = [];

    foreach ($xml_arr->record as $r) {
        $temperature = (float)$r->sensor->temperature;
        $humidity = (float)$r->sensor->humidity;
        $condition = (string)$r->sensor->condition;
        $timestamp = (string)$r->sensor->timestamp;
        $temperature_threshold = (float)$r->sensor->temperature_threshold;
        $humidity_threshold = (float)$r->sensor->humidity_threshold; 

        if ($temperature > $temperature_threshold || $humidity > $humidity_threshold) {
            $above_threshold_data[] = [
                'timestamp' => $timestamp,
                'temperature' => $temperature,
                'humidity' => $humidity,
                'condition' => $condition
            ];
        }

        if ($condition == "collision") {
            $collision_data[] = [
                'timestamp' => $timestamp,
                'temperature' => $temperature,
                'humidity' => $humidity,
                'condition' => $condition
            ];
        }

        if ($condition == "windy") {
            $high_wind_data[] = [
                'timestamp' => $timestamp,
                'temperature' => $temperature,
                'humidity' => $humidity,
                'condition' => $condition
            ];
        }
    }

    // Display tables
    createTable($above_threshold_data, 'Timestamps Above Threshold');
    createTable($collision_data, 'Collision Events');
    createTable($high_wind_data, 'High Wind States');

    // Display additional information with styling
    echo '<div class="info">';
    echo "<h2>Additional Information</h2>";
    echo "<p>Total number of timestamps recorded: <span>$total_timestamps</span></p>";
    echo "<p>Current temperature threshold: <span>$temperature_threshold &deg;C</span></p>";
    echo "<p>Current humidity threshold: <span>$humidity_threshold %</span></p>";
    echo '</div>';
} else {
    echo "<div class='info'>";
    echo "<p>No sensor data available.</p>";
    echo '</div>';
}
?>
