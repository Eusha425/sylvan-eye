<?php 
	error_reporting(E_ALL);						//show any errors if there is any
	ini_set('display_errors', '1');


	if(isset($_GET['temperature']) && isset($_GET['humidity']) && isset($_GET['condition']) && isset($_GET['timestamp'])) { 					// Check if temprature is present or not
		
		$str = '';								// intialize empty string


		if(file_exists('sensorData.xml')) {				// if the xml file already exists then read it
			$str = file_get_contents('sensorData.xml');	// get all the current data
		}
		
		if(strlen($str) == 0) {
			// intialize the variable to the empty xml if there is no old content
			$str = "<?xml version='1.0' encoding='UTF-8'?> \n<records></records>";
		}

		// create a new text for appending to the file
		$newData = "\n<record>\n<sensor>\n<temperature>". $_GET['temperature']. "</temperature>\n<humidity>". $_GET['humidity']."</humidity>\n<condition>". $_GET['condition'] ."</condition>\n". "<timestamp>". $_GET['timestamp'] ."</timestamp>\n</sensor>\n<date>". date('d-m-Y H:i:s') . "</date>\n</record>\n</records>"; 	
		$str = str_replace("</records>", $newData, $str);	// put the data in the end of the xml document
		
		file_put_contents('sensorData.xml', $str);			// write the file back to the server

		echo '1';							// return success
	}
	else
		echo '0';							// return failure
?>
