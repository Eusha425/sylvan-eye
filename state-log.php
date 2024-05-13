<?php
	$filename = "state.txt";
	if(isset($_GET['state']))
	{
		$state = $_GET['state'];
		file_put_contents($filename, $state.PHP_EOL, FILE_APPEND);
		echo "Write Successful";
	}
	else
	{
		echo "Unsuccessful";
	}
	
?>
