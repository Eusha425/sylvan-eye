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
    acc = s.get_accelerometer()
    x = round(acc['pitch'],2)
    y = round(acc['yaw'],2)
    z = round(acc['roll'],2)
    if (abs(x - in_x) > 0.3 or abs(y - in_y) > 0.3 or abs(z - in_z) > 0.3):
        state = 'collision'
        s.show_message("Collision")
        #report collision to server
        upload(state)
        
        #payload = {'state' : state}
        #sr = req.get(server, params = payload)
        
        for event in s.stick.get_events():
            if event.action == "pressed" and event.direction == "middle":
                state = 'normal'
                s.clear()
                print(state)    
    elif(abs(x - in_x) > 0.1 or abs(y - in_y) > 0.1 or abs(z - in_z) > 0.1):
        state = 'windy'
        # report to server here
        upload(state)
        #payload = {'state' : state}
        #sr = req.get(server, params = payload)
        state = 'normal' # changing state to normal after reporting to the server
        # print(sr.text)
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

