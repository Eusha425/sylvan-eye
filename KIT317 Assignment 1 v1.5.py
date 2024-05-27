from sense_emu import SenseHat
import requests as req
import time

temp_thresh = 15
humidity_thresh = 100

def setup():
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
                        
                        
def movement():
    s = SenseHat()
    in_x = in_y = in_z = 0
    state = 'normal'
    collision_flag = False


    acc = s.get_accelerometer_raw()
    x = round(acc['x'], 2)
    y = round(acc['y'], 2)
    z = round(acc['z'], 2)

    max_diff = max(abs(x - in_x), abs(y - in_y), abs(z - in_z))

    if max_diff > 0.3:
        if state != 'collision':
            state = 'collision'
            collision_flag = True  # Set flag to indicate collision
            if collision_flag:
                s.show_message("Collision")
                
            # report collision to server
            upload(state)
            while collision_flag:
                for event in s.stick.get_events():
                    if event.action == "pressed" and event.direction == "middle":
                        if collision_flag:  # Only clear if a collision occurred
                            state = 'normal'
                            s.clear()
                            collision_flag = False  # Reset collision flag
                            print(state)
        print(state)

    elif max_diff > 0.1:
        if state != 'windy':
            state = 'windy'
            # report windy state to server
            upload(state)
        print(state)

    else:
        if state != 'normal' and not collision_flag:
            state = 'normal'
            print(state)

    

    in_x = x
    in_y = y
    in_z = z
    
def main():
    s = SenseHat()
    setup_mode = False
    while True:
        
                
        if setup_mode == False:
            movement()
        
            
        for event in s.stick.get_events():
            
            if event.action in ('pressed') and event.direction in ('middle'):
                print("In Setup")
                initial_time = time.time()
                setup()
                    

def upload(status):
    global temp_thresh
    global humidity_thresh
    
    server = 'http://iotserver.com/webserver.php'
    s = SenseHat()

    state = status #default value until connected with part 1
    
    t_time = time.strftime("%H:%M:%S")
    temp = s.get_temperature ()
    humidity = s.get_humidity()
    payload = {'temperature' : temp, 'humidity' : humidity, 'condition':state, 'timestamp' : t_time, 'temp_thresh' : temp_thresh, 'humidity_thresh': humidity_thresh}
    r = req.get(server, params = payload)
    if r.text == '0':
        
        print("Error adding data to the server")
    else: # else statement here just to check if data uploaded
        print("Data added")
    #time.sleep(0.60) # sleep time needs to change to reflect the 1 min time requirement

main()
