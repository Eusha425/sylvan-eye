<?php
error_reporting(E_ALL);
ini_set('display_errors', '1');

$xml_arr = '';

if (file_exists('sensorData.xml')) {
    $xml_arr = simplexml_load_file('sensorData.xml');

    // Start the HTML table
    echo '<table border="1">';
    echo '<tr>';
    echo '<th>Temperature</th>';
    echo '<th>Humidity</th>';
    echo '<th>Condition</th>';
    echo '<th>Timestamp</th>';
    echo '<th>Date</th>';
    echo '</tr>';

    foreach ($xml_arr->record as $r) {
        // Display each row of data in the table
        echo '<tr>';
        echo '<td>' . $r->sensor->temperature . '</td>';
        echo '<td>' . $r->sensor->humidity . '</td>';
        echo '<td>' . $r->sensor->condition . '</td>';
        echo '<td>' . $r->sensor->timestamp . '</td>';
        echo '<td>' . $r->date . '</td>';
        echo '</tr>';
    }

    // End the HTML table
    echo '</table>';
} else {
    echo "No file";
}
?>
