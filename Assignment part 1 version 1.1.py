from sense_emu import SenseHat
import requests as req

server = 'http://iotserver.com/state-log.php'
s = SenseHat()
in_x = in_y = in_z = 0
state = 'normal'

while True:
    acc = s.get_accelerometer_raw()
    x = round(acc['x'],2)
    y = round(acc['y'],2)
    z = round(acc['z'],2)
    if (abs(x - in_x) > 0.3 or abs(y - in_y) > 0.3 or abs(z - in_z) > 0.3):
        state = 'collision'
        s.show_message("Collision")
        #report collision to server
        payload = {'state' : state}
        sr = req.get(server, params = payload)
        for event in s.stick.get_events():
            if event.direction in ('middle'):
                state = 'normal'
                s.clear(0,0,0)
                print(state)
        
    elif(abs(x - in_x) > 0.1 or abs(y - in_y) > 0.1 or abs(z - in_z) > 0.1):
        state = 'windy'
        # report to server here 
        payload = {'state' : state}
        sr = req.get(server, params = payload)
        state = 'normal' # changing state to normal after reporting to the server
        # print(sr.text)
        print(state)
    else:
        state = 'normal'
    in_x = x
    in_y = y
    in_z = z
