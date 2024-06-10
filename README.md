# IoT Environmental Sensor and Webserver

This project is a prototype for a sensor device designed to assist forestry workers in monitoring the growing conditions of trees. The device, emulated using the Sense HAT, collects environmental data and communicates with a webserver to log and display the data. The webserver, implemented in PHP, logs the data received from the sensor and provides a user interface to view the log.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
  - [IoT Device](#iot-device)
  - [Webserver](#webserver)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
  - [IoT Device](#iot-device-usage)
  - [Webserver](#webserver-usage)
- [Files](#files)
- [System Diagram](#system-diagram)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project involves creating an IoT device that uses the Sense HAT emulator to take environmental readings and report them back to a webserver. The device detects movement events in real-time, classifies the movement, and reports it to the server. The webserver logs these events and provides a way to view the log, including details such as temperature, humidity, and wind conditions.

## Features

### IoT Device

- Detects movement events and classifies them as normal, windy, or collision based on movement change thresholds.
- Reports environmental data (temperature, humidity, wind conditions) to the server every minute.
- Displays errors if the server does not acknowledge the report.
- Contains a setup mode to adjust temperature and humidity thresholds.

### Webserver

- Receives updates from the IoT device and logs the data in an XML file.
- Provides a view of the log, including the total number of timestamps recorded, current temperature and humidity thresholds, and details of events that exceed the thresholds or involve collisions.

## Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Eusha425/iot-environmental-sensor.git
   cd iot-environmental-sensor
2. **Install Dependencies**
- For the IoT device (Python):
  ```bash
  pip install sense_hat
- For the websever (PHP):
  Ensure you have a web server (e.g. Apache) and PHP installed.
3. **Start the webserver**
- Place the webserver.php and displaywebserver.php files in your web server's root directory (e.g., /var/www/html for Apache).
4. **Run the IoT Device Script**
   ```bash
   python iot_device.py

## Usage
### IoT Device Usage
- **Normal Operation Mode:** The device reports environmental data to the server every minute.
- **Setup Mode:** Entered by pressing the middle button on the Sense HAT while not in a collision state. Use the left and right buttons to switch between temperature and humidity modes, and the up and down buttons to adjust the thresholds. Press the middle button again to exit setup mode.

### Webserver Usage
- Access the **`displaywebserver.php`** file through your web browser to view the logged data.

### Files
- **`iot_device.py`**: The Python script for the IoT device.
- **`webserver.php`**: The PHP script for receiving data from the IoT device and logging it.
- **`displaywebserver.php`**: The PHP script for displaying the logged data.

## System Diagram
[State transistion diagram](./assets/State%20Diagram.pdf)

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss any changes or enhancements.

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
