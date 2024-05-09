from sense_emu import SenseHat
import requests as req
import time

state = 'normal'
s = SenseHat()
temp_thresh = 1
humidity_thresh = 1
setup = False
left = False
right = False

while True:
    for event in s.stick.get_events():
        
        # to get into setup mode and exit it upon pressing the middle button
        if setup == False and event.direction in ('middle') and event.action in ('pressed'):
            setup = True
            print("In Setup mode")
        elif setup == True and event.direction in ('middle') and event.action in ('pressed'):
            setup = False
            print("Exit Setup")
            
        if setup == True:
            
            #into the temp mode
            if event.direction in ('left') and event.action in ('pressed'):
                s.show_message("Temperature")
                left = True
                
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
            if right == True:
                if event.direction in ('up') and event.action in ('pressed'):
                    humidity_thresh +=1
                    print(f"Humidity Thresh:{humidity_thresh}")
                    s.show_message(str(humidity_thresh))
                    
                elif event.direction in ('down') and event.action in ('pressed'):
                    humidity_thresh -= 1
                    print(f"Humidity Thresh:{humidity_thresh}")
                    s.show_message(str(humidity_thresh))
        
