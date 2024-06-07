from sense_emu import SenseHat  # using Sense Emulator
import time
import requests as req

temp_thresh = 20
humidity_thresh = 10

sense = SenseHat()

last_x = sense.accel_raw['x']
last_y = sense.accel_raw['y']
last_z = sense.accel_raw['z']

collision_state = False
setup = False
humidity = False
temp = False
state ="normal"

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
    
    if event.action == 'pressed':
        if humidity:
            humidity_thresh += 1
            print(f"humidity thresh {humidity_thresh}")
        elif temp:
            temp_thresh += 1
            print(f"temp thresh {temp_thresh}")
        
def decrease_thresh(event):
    global humidity
    global humidity_thresh
    global temp_thresh
    global temp
    
    if event.action == 'pressed':
        if humidity:
            humidity_thresh -= 1
            print(f"humidity thresh {humidity_thresh}")
        elif temp:
            temp_thresh -= 1
            print(f"temp thresh {temp_thresh}")

def humidity_mode(event):
    global setup
    global humidity
    global temp
    if event.action == 'pressed':
        if setup:
            
            sense.show_message("Humidity", scroll_speed=0.070)
            humidity = True
            temp = False
            

def temp_mode(event):
    global setup
    global humidity
    global temp
    if event.action == 'pressed':
        if setup:
            
            sense.show_message("Temperature", scroll_speed=0.070)
            temp = True
            humidity = False
            
        

def setup_mode(event):
    global setup
    global temp
    global humidity
    
    if event.action == 'pressed':
        if collision_state == False:
            if setup != True:
                setup = True
                print("first press")
                print(setup)
            else:
                setup = False
                temp = False
                humidity = False
                print("second")
                print(setup)

            
def report_state():
    
    global temp_thresh
    global humidity_thresh
    global state
    print("State reported to server:", state)
    server = 'http://iotserver.com/webserver.php'
    s = SenseHat()

    t_time = time.strftime("%H:%M:%S")
    temp = s.get_temperature()
    humidity = s.get_humidity()
    payload = {'temperature': temp, 'humidity': humidity, 'condition': state, 'timestamp': t_time,
               'temp_thresh': temp_thresh, 'humidity_thresh': humidity_thresh}
    r = req.get(server, params=payload)
    if r.text == '0':
        print("Error adding data to the server")
    else:
        print("Data added")
        if state == "windy":
            state = "normal"
    return        


last_upload_time = time.time()
while True:
    current_time = time.time()
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
                if current_time - last_upload_time >= 15:
                    
                    report_state()
                    last_upload_time = current_time
                current_time = time.time()
        
            
    elif change > 0.1:
        state = "windy"
        print(state)
    else:
        #state = "normal"
        #print('test')
        sense.stick.direction_middle = setup_mode
        sense.stick.direction_right = humidity_mode
        sense.stick.direction_left = temp_mode
        sense.stick.direction_up = increase_thresh
        sense.stick.direction_down = decrease_thresh
        time.sleep(1)            
    last_x = x
    last_y = y
    last_z = z
    
    if current_time - last_upload_time >= 15:        
        if setup != True:
            report_state()
        last_upload_time = current_time
    #print(f"change is {change}")
    #print("State:", state)
    
    
    
    