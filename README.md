# Forestry Monitor (IoT Device and Webserver)
KIT317 Assignment 1: Forestry Monitor (IoT Device and Webserver)

## Overview
This repository contains the code for a prototype IoT device and a webserver designed to monitor growing conditions for trees. It simulates a SenseHat device and interacts with a webserver implemented in PHP.

## Project Purpose
The primary objective of this assignment is to create a system that:

- Emulates an IoT device capable of reading environmental data (temperature, humidity) and detecting movement (windy/collision).
- Reports data to a webserver at regular intervals.
- Implements a setup mode for configuring thresholds for temperature and humidity.
- Logs data received from the device on the webserver.
- Provides a user interface to view logged data and device thresholds.

## Functionality

### SenseHat Device (Python):
- Detects real-time movement and classifies it as normal, windy, or collision.
- Reports temperature, humidity, and wind conditions to the webserver every minute.
- Displays error messages if acknowledgment is not received from the server.
- Enters a setup mode for configuring thresholds.
- Changes between temperature and humidity modes.
- Adjusts thresholds based on button presses.
- Times out and exits setup mode after inactivity.

### Webserver (PHP):
- Receives data from the SenseHat device and logs it to an XML file.
- Acknowledges data reception to the device.
- Provides a viewable log displaying:
  - Timestamps for recorded data.
  - Events exceeding temperature/humidity thresholds.
  - Collision events.
  - Total high wind states.
- Displays current temperature and humidity thresholds.

## Files
- `sensehat_device.py`: Python code for the SenseHat device simulation.
- `webserver.php`: PHP code for the webserver.
- `system_diagram.[file extension]`: Diagram depicting the system workflow (replace with actual file extension, e.g., png, jpg).
- `assignment_demo.mp4`: Video demonstrating the project functionalities (replace with actual file extension).

## Dependencies
- Python libraries (refer to `sensehat_device.py` for specific ones).
- PHP libraries (refer to `webserver.php` for specific ones).

## Instructions
1. Ensure you have the required libraries installed for Python and PHP.
2. Run the `sensehat_device.py` script to start the simulated device.
3. Start the webserver using a PHP development server (instructions vary based on your setup).
4. Interact with the SenseHat device simulation (buttons) to observe its behavior.
5. Access the webserver in your browser to view logged data and thresholds.

## Note
This README provides a general overview. Refer to the code comments for detailed implementation specifics.

## Academic Integrity Warning
This repository is intended for use as an assignment for a specific course. Any individual using the code in this repository to complete their own assignment without proper citation and authorization may be violating academic integrity policies and may be subject to consequences as outlined by their academic institution.
