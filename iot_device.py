# Name: Gazi MD Wasi-UL-Hoque Eusha
# Student ID: 624121
# Version: 1.4

# importing libraries needed for the program

from sense_emu import SenseHat  # using Sense Emulator
import time
import requests as req

#constants declared
SETUP_MODE_TIMEOUT = 10 # time when the setup mode is going to timeout and exit
SERVER_SEND_TIME = 15   # time when the program is going to update the status to the server

temp_thresh = 20        # initial temperature threshold value
humidity_thresh = 10    # initial humidity threshold value

sense = SenseHat()      # instantiating a sense hat object

# getting the yaw, pitch and roll values from the IMU(Inertial Measurement Unit)
last_x = sense.accel_raw['x']
last_y = sense.accel_raw['y']
last_z = sense.accel_raw['z']

# initial state values
collision_state = False
setup = False
humidity = False
temp = False
state ="normal"

# time initiations to track button presses
last_button_press = time.time()  # To track when a button has been pressed when in setup mode so that it can timeout and exit at the correct interval
last_upload_time = time.time() # to track when the value has been last uploaded to the server


# when middle button is pressed, so that the collision statues gets cleared
def handle_collision(event):
    global collision_state
    global state
    if event.action == 'pressed':
        if setup == False:
            print("collision message cleared")
            sense.clear()
            collision_state = False
            state = "normal"
            print(state)


def increase_thresh(event):
    global humidity
    global humidity_thresh
    global temp_thresh
    global temp
    global last_button_press
    global sense
    
    if event.action == 'pressed':
        last_button_press = time.time()  # Update last button press time
        if humidity == True:
            humidity_thresh += 1
            print(f"humidity thresh {humidity_thresh}")
            sense.show_message(str(humidity_thresh), scroll_speed=0.070)
        elif temp == True:
            temp_thresh += 1
            print(f"temp thresh {temp_thresh}")
            sense.show_message(str(temp_thresh), scroll_speed=0.070)


def decrease_thresh(event):
    global humidity
    global humidity_thresh
    global temp_thresh
    global temp
    global last_button_press
    global sense
    
    if event.action == 'pressed':
        last_button_press = time.time()  # Update last button press time
        if humidity == True:
            humidity_thresh -= 1
            print(f"humidity thresh {humidity_thresh}")
            sense.show_message(str(humidity_thresh), scroll_speed=0.070)
        elif temp == True:
            temp_thresh -= 1
            print(f"temp thresh {temp_thresh}")
            sense.show_message(str(temp_thresh), scroll_speed=0.070)


def humidity_mode(event):
    global setup
    global humidity
    global temp
    global last_button_press
    
    if event.action == 'pressed':
        if setup:
            last_button_press = time.time()  # Update last button press time
            sense.show_message("Humidity", scroll_speed=0.070)
            humidity = True
            temp = False
            

def temp_mode(event):
    global setup
    global humidity
    global temp
    global last_button_press
    
    if event.action == 'pressed':
        if setup:
            last_button_press = time.time()  # Update last button press time
            sense.show_message("Temperature", scroll_speed=0.070)
            temp = True
            
            humidity = False


def setup_mode(event):
    global setup
    global temp
    global humidity
    global last_button_press
    
    if event.action == 'pressed':
        if collision_state == False:
            if setup != True:
                setup = True
                print("Setup Mode")
                print(setup)
                last_button_press = time.time()
            else:
                setup = False
                temp = False
                humidity = False
                print("Exit Setup")
                print(setup)

            
def report_state(temperature_data,humidity_data):
    global temp_thresh
    global humidity_thresh
    global state
    print("State reported to server:", state)
    server = 'http://iotserver.com/webserver.php'
    

    t_time = time.strftime("%H:%M:%S")
    payload = {'temperature': temperature_data, 'humidity': humidity_data, 'condition': state, 'timestamp': t_time,
               'temp_thresh': temp_thresh, 'humidity_thresh': humidity_thresh}
    
    r = req.get(server, params=payload)
    if r.text == '0':
        print("Error adding data to the server")
    else:
        print("Data added")
        if state == "windy":
            state = "normal"


sense.show_message("Monitoring Start", scroll_speed = 0.09)
while True:
    current_time = time.time()
    
    temperature_data = sense.get_temperature()
    humidity_data = sense.get_humidity()
    
    if current_time - last_upload_time >= SERVER_SEND_TIME:
        if not setup:
            report_state(temperature_data,humidity_data)
        last_upload_time = current_time
        
    
    x = sense.accel_raw['x']
    y = sense.accel_raw['y']
    z = sense.accel_raw['z']
    change = abs(x - last_x) + abs(y - last_y) + abs(z - last_z)
    
    if change > 0.3:
        collision_state = True
        state = "collision"
        print("State:", state)
        while collision_state:
            sense.show_message("Collision", scroll_speed=0.070)
            
            if collision_state:
                print(state)
                sense.stick.direction_middle = handle_collision
                if current_time - last_upload_time >= SERVER_SEND_TIME:
                    
                    report_state(temperature_data,humidity_data)
                    last_upload_time = current_time
                current_time = time.time()

    elif change > 0.1:
        state = "windy"
        print(state)
    
    if setup:
        if current_time - last_button_press >= SETUP_MODE_TIMEOUT:
            print("Setup mode timed out")
            setup = False
            temp = False
            humidity = False
    else:
        #state = "normal"
        #print('test')
        sense.stick.direction_middle = setup_mode
        sense.stick.direction_right = humidity_mode
        sense.stick.direction_left = temp_mode
        sense.stick.direction_up = increase_thresh
        sense.stick.direction_down = decrease_thresh
    
    last_x = x
    last_y = y
    last_z = z

    time.sleep(1)
