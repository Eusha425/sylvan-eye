<?php 

	error_reporting(E_ALL);									//show any errors if there is any
	ini_set('display_errors', '1');
	
		$xml_arr = '';										// intialize empty string


		if(file_exists('sensorData.xml')) {					// if the xml file already exists then read it
			$xml_arr = simplexml_load_file('sensorData.xml');	// get all the current data

			foreach($xml_arr->record as $r) {				
				// display the data				
				echo $r->sensor->temperature . ", " . $r->sensor->humidity . ", " . $r->sensor->condition . ", " . $r->sensor->timestamp . ", " . $r->date. "<br/>\n";
			}
		}
		else {
			echo "No file";
		}
?>
