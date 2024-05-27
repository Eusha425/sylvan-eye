from sense_emu import SenseHat  # using Sense Emulator
import time
import requests as req

temp_thresh = 20
humidity_thresh = 10

class EnvironmentalSensor:
    def __init__(self):
        self.sense = SenseHat()
        self.last_x = self.sense.accel_raw['x']
        self.last_y = self.sense.accel_raw['y']
        self.last_z = self.sense.accel_raw['z']
        self.state = "normal"
        self.in_collision_mode = False

    def detect_movement(self):
        x = self.sense.accel_raw['x']
        y = self.sense.accel_raw['y']
        z = self.sense.accel_raw['z']

        change = abs(x - self.last_x) + abs(y - self.last_y) + abs(z - self.last_z)

        if change > 0.3:
            self.state = "collision"
            #self.report_state()
            if not self.in_collision_mode:
                self.in_collision_mode = True
                self.show_collision_message()
                self.handle_middle_button_press()  # Call the function to handle middle button press
        elif change > 0.1:
            self.state = "windy"
            #self.report_state()
            self.in_collision_mode = False
        else:
            if self.state == "normal":
                for event in self.sense.stick.get_events():
                    if event.direction == 'middle' and event.action == 'pressed':
                        self.setup()  # Enter setup mode only if middle button pressed and state is "normal"
                        break
        self.in_collision_mode = False

        self.last_x = x
        self.last_y = y
        self.last_z = z

        print("State:", self.state)
        #print("Change:", change)
        #print("Acceleration (x,y,z):", x, y, z)
        #print("------------------------------")
        
        
    def setup(self):
        global temp_thresh
        global humidity_thresh
        
        initial_time = time.time()
        last_activity_time = initial_time  # Track the last activity time
        
        s = SenseHat()
        
        setup = True
        left = False
        right = False

        while setup:
            # Record the current time
            current_time = time.time()
            # Check if setup mode should exit due to inactivity
            if current_time - last_activity_time > 10:
                setup = False
                print("Exit Setup due to inactivity")
                break
            
            for event in s.stick.get_events():
                last_activity_time = time.time()  # Update the last activity time
                
                # Check if setup mode should exit due to button press
                if setup and event.direction == 'middle' and event.action == 'pressed':
                    setup = False
                    print("Exit Setup")
                    break
                    
                if setup:
                    # Into the temp mode
                    if event.direction == 'left' and event.action == 'pressed':
                        s.show_message("Temperature")
                        left = True
                        right = False
                        
                    if left:
                        if event.direction == 'up' and event.action == 'pressed':
                            temp_thresh += 1
                            print(f"Temp Thresh:{temp_thresh}")
                            s.show_message(str(temp_thresh))
                            
                        elif event.direction == 'down' and event.action == 'pressed':
                            temp_thresh -= 1
                            print(f"Temp Thresh:{temp_thresh}")
                            s.show_message(str(temp_thresh))
                            
                    # Into the humidity mode
                    if event.direction == 'right' and event.action == 'pressed':
                        s.show_message("Humidity")
                        right = True
                        left = False
                    if right:
                        if event.direction == 'up' and event.action == 'pressed':
                            humidity_thresh += 1
                            print(f"Humidity Thresh:{humidity_thresh}")
                            s.show_message(str(humidity_thresh))
                            
                        elif event.direction == 'down' and event.action == 'pressed':
                            humidity_thresh -= 1
                            print(f"Humidity Thresh:{humidity_thresh}")
                            s.show_message(str(humidity_thresh))
    
    
    def report_state(self):
        global temp_thresh
        global humidity_thresh
        print("State reported to server:", self.state)
        server = 'http://iotserver.com/webserver.php'
        s = SenseHat()

        t_time = time.strftime("%H:%M:%S")
        temp = s.get_temperature()
        humidity = s.get_humidity()
        payload = {'temperature': temp, 'humidity': humidity, 'condition': self.state, 'timestamp': t_time,
                   'temp_thresh': temp_thresh, 'humidity_thresh': humidity_thresh}
        r = req.get(server, params=payload)
        if r.text == '0':
            print("Error adding data to the server")
        else:
            print("Data added")
            if self.state == "windy":
                self.state = "normal"  # Return state to "normal" after successful report

    def show_collision_message(self):
        self.sense.show_message("Collision Detected!", text_colour=(255, 0, 0))
        

    def clear_collision_message(self):
        self.sense.clear()
        self.in_collision_mode = False
        print("Collision message cleared.")

    def handle_middle_button_press(self):
        while self.in_collision_mode:
            for event in self.sense.stick.get_events():
                if event.action == "pressed" and event.direction == "middle":
                    self.clear_collision_message()
                    self.state = "normal"  # Switch back to "normal" state when the middle button is pressed
                    return

    def run(self):
        last_upload_time = time.time()  # Initialize last upload time
        while True:
            self.detect_movement()
            current_time = time.time()
            if current_time - last_upload_time >= 15:  # Check if 1 minute has elapsed
                self.report_state()
                last_upload_time = current_time  # Update last upload time
            time.sleep(1)

if __name__ == "__main__":
    sensor = EnvironmentalSensor()
    sensor.run()
