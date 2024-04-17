from sense_emu import SenseHat
import requests as req
import time

state = 'normal'
s = SenseHat()
temp_thresh = 1
humidity_thresh = 1

while True:
    for event in s.stick.get_events():
        if event.direction in ('left'):
            s.show_message("Temperature")
            if event.direction in ('up'):
                temp_thresh += 1
                s.show_message(temp_thresh)
            elif event.direction in ('down'):
                temp_thresh -= 1
        elif event.direction in ('right'):
            s.show_message("Humidity")
            
    