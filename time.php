<?php
	$filename = "time.txt";
	if(isset($_GET['temp']) && isset($_GET['humidity']) && isset($_GET['time']))
	{
		$time = $_GET['time'];
		$temp = $_GET['temp'];
		$humidity = $_GET['humidity'];
		$data = $time . " " . $temp . " " . $humidity;
		
		file_put_contents($filename, $data.PHP_EOL, FILE_APPEND);
		echo "Write Successful";
	}
	else
	{
		echo "Unsuccessful";
	}
	
?>
