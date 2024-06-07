from sense_emu import SenseHat  # using Sense Emulator
import time
import requests as req

class EnvironmentalSensor:
    def __init__(self):
        self.sense = SenseHat()
        self.last_x = self.sense.accel_raw['x']
        self.last_y = self.sense.accel_raw['y']
        self.last_z = self.sense.accel_raw['z']
        self.state = "normal"
        self.in_collision_mode = False
        self.temp_thresh = 20
        self.humidity_thresh = 10

    def detect_movement(self):
        x = self.sense.accel_raw['x']
        y = self.sense.accel_raw['y']
        z = self.sense.accel_raw['z']

        change = abs(x - self.last_x) + abs(y - self.last_y) + abs(z - self.last_z)

        if change > 0.3:
            self.state = "collision"
            print("State:", self.state)
            if not self.in_collision_mode:
                self.in_collision_mode = True
                self.show_collision_message()
                self.handle_middle_button_press()
        elif change > 0.1:
            self.state = "windy"
            self.in_collision_mode = False
        else:
            if self.state == "normal":
                for event in self.sense.stick.get_events():
                    if event.direction == 'middle' and event.action == 'pressed':
                        self.sense.show_message("Setup Mode", scroll_speed=0.070)
                        print("In Setup")
                        self.setup()
                        break
        self.in_collision_mode = False

        self.last_x = x
        self.last_y = y
        self.last_z = z

        print("State:", self.state)

    def setup(self):
        initial_time = time.time()
        last_activity_time = initial_time
        setup = True
        left = False
        right = False

        while setup:
            current_time = time.time()
            if current_time - last_activity_time > 10:
                setup = False
                print("Exit Setup due to inactivity")
                return self.run()

            for event in self.sense.stick.get_events():
                last_activity_time = time.time()

                if setup and event.direction == 'middle' and event.action == 'pressed':
                    setup = False
                    print("Exit Setup")
                    return self.run()

                if setup:
                    if event.direction == 'left' and event.action == 'pressed':
                        self.sense.show_message("Temperature")
                        left = True
                        right = False

                    if left:
                        if event.direction == 'up' and event.action == 'pressed':
                            self.temp_thresh += 1
                            print(f"Temp Thresh:{self.temp_thresh}")
                            self.sense.show_message(str(self.temp_thresh))

                        elif event.direction == 'down' and event.action == 'pressed':
                            self.temp_thresh -= 1
                            print(f"Temp Thresh:{self.temp_thresh}")
                            self.sense.show_message(str(self.temp_thresh))

                    if event.direction == 'right' and event.action == 'pressed':
                        self.sense.show_message("Humidity")
                        right = True
                        left = False
                    if right:
                        if event.direction == 'up' and event.action == 'pressed':
                            self.humidity_thresh += 1
                            print(f"Humidity Thresh:{self.humidity_thresh}")
                            self.sense.show_message(str(self.humidity_thresh))

                        elif event.direction == 'down' and event.action == 'pressed':
                            self.humidity_thresh -= 1
                            print(f"Humidity Thresh:{self.humidity_thresh}")
                            self.sense.show_message(str(self.humidity_thresh))

    def report_state(self):
        print("State reported to server:", self.state)
        server = 'http://iotserver.com/webserver.php'
        s = SenseHat()

        t_time = time.strftime("%H:%M:%S")
        temp = s.get_temperature()
        humidity = s.get_humidity()
        payload = {'temperature': temp, 'humidity': humidity, 'condition': self.state, 'timestamp': t_time,
                   'temp_thresh': self.temp_thresh, 'humidity_thresh': self.humidity_thresh}
        r = req.get(server, params=payload)
        if r.text == '0':
            print("Error adding data to the server")
        else:
            print("Data added")
            if self.state == "windy":
                self.state = "normal"
        return

    def show_collision_message(self):
        if self.in_collision_mode:
            self.sense.show_message("Collision Detected!", text_colour=(255, 0, 0), scroll_speed=0.070)

    def clear_collision_message(self):
        self.in_collision_mode = False
        self.state = "normal"
        print("Collision message cleared.")
        self.sense.clear()
        return  

    def handle_middle_button_press(self):
        last_upload_time = time.time()
        while self.in_collision_mode:
            current_time = time.time()
            if current_time - last_upload_time >= 15:
                self.report_state()
                last_upload_time = current_time
            for event in self.sense.stick.get_events():
                if event.action == "pressed" and event.direction == "middle":
                    self.clear_collision_message()
                    return self.run()

    def run(self):
        last_upload_time = time.time()
        while True:
            self.detect_movement()
            current_time = time.time()
            if current_time - last_upload_time >= 15:
                self.report_state()
                last_upload_time = current_time
            time.sleep(1)

if __name__ == "__main__":
    sensor = EnvironmentalSensor()
    sensor.run()
