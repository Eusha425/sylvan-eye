from sense_hat import SenseHat
import time

sense = SenseHat()

# Define thresholds and initial values
temp_threshold = 25
humidity_threshold = 50
current_mode = "temperature"  # Initial mode

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Function to display mode and threshold
def display_mode_threshold():
    if current_mode == "temperature":
        sense.show_message("TEMP: " + str(temp_threshold), text_colour=BLUE)
    else:
        sense.show_message("HUMIDITY: " + str(humidity_threshold), text_colour=GREEN)

# Function to handle setup mode
def setup_mode():
    global temp_threshold, humidity_threshold, current_mode
    
    sense.clear()
    display_mode_threshold()
    
    while True:
        events = sense.stick.get_events()
        
        # Check if no button has been pressed for 10 seconds
        if not events:
            time.sleep(10)
            break
        
        for event in events:
            if event.action == "pressed":
                if event.direction == "left" or event.direction == "right":
                    # Toggle mode between temperature and humidity
                    current_mode = "temperature" if current_mode == "humidity" else "humidity"
                    display_mode_threshold()
                elif event.direction == "up":
                    # Increase threshold
                    if current_mode == "temperature":
                        temp_threshold += 1
                    else:
                        humidity_threshold += 1
                    display_mode_threshold()
                elif event.direction == "down":
                    # Decrease threshold
                    if current_mode == "temperature":
                        temp_threshold -= 1
                    else:
                        humidity_threshold -= 1
                    display_mode_threshold()
                elif event.direction == "middle":
                    return

# Main loop
while True:
    events = sense.stick.get_events()
    
    for event in events:
        if event.action == "pressed" and event.direction == "middle":
            setup_mode()
            
    # Normal operation mode
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
    
    # Check collision state (This part is not implemented in the provided code)
    collision_state = False  # Assuming no collision detection
    
    if not collision_state:
        if current_mode == "temperature":
            if temperature > temp_threshold:
                # Perform action for temperature threshold exceeded
                print("Temperature threshold exceeded:", temperature)
        else:
            if humidity > humidity_threshold:
                # Perform action for humidity threshold exceeded
                print("Humidity threshold exceeded:", humidity)
