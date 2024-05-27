from sense_emu import SenseHat
import requests as req
import time

def setup():
    s = SenseHat()
    temp_thresh = 1
    humidity_thresh = 1
    setup = True
    left = False
    right = False

    while setup == True:
        for event in s.stick.get_events():
            
            # to get into setup mode and exit it upon pressing the middle button
            
            if setup == True and event.direction in ('middle') and event.action in ('pressed'):
                setup = False
                print("Exit Setup")
                break
                
                
            if setup == True:
                
                #into the temp mode
                if event.direction in ('left') and event.action in ('pressed'):
                    s.show_message("Temperature")
                    left = True
                    right = False
                    
                if left == True:
                    if event.direction in ('up') and event.action in ('pressed'):
                        temp_thresh +=1
                        print(f"Temp Thresh:{temp_thresh}")
                        s.show_message(str(temp_thresh))
                        
                    elif event.direction in ('down') and event.action in ('pressed'):
                        temp_thresh -= 1
                        print(f"Temp Thresh:{temp_thresh}")
                        s.show_message(str(temp_thresh))
                        
                # into the humidity mode
                if event.direction in ('right') and event.action in ('pressed'):
                    s.show_message("Humidity")
                    right = True
                    left = False
                if right == True:
                    if event.direction in ('up') and event.action in ('pressed'):
                        humidity_thresh +=1
                        print(f"Humidity Thresh:{humidity_thresh}")
                        s.show_message(str(humidity_thresh))
                        
                    elif event.direction in ('down') and event.action in ('pressed'):
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
                setup()
                    



def upload(status):
    server = 'http://iotserver.com/webserver.php'
    s = SenseHat()

    state = status #default value until connected with part 1
    
    t_time = time.strftime("%H:%M:%S")
    temp = s.get_temperature ()
    humidity = s.get_humidity()
    payload = {'temperature' : temp, 'humidity' : humidity, 'condition':state, 'timestamp' : t_time}
    r = req.get(server, params = payload)
    if r.text == '0':
        
        print("Error adding data to the server")
    else: # else statement here just to check if data uploaded
        print("Data added")
    #time.sleep(0.60) # sleep time needs to change to reflect the 1 min time requirement

main()

