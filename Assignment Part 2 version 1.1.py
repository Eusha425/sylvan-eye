from sense_emu import SenseHat
import requests as req
import time

server = 'http://iotserver.com/webserver.php'
s = SenseHat()

state = 'normal' #default value until connected with part 1
while True:
    t_time = time.strftime("%H:%M:%S")
    temp = s.get_temperature ()
    humidity = s.get_humidity()
    payload = {'temperature' : temp, 'humidity' : humidity, 'condition':state, 'timestamp' : t_time}
    r = req.get(server, params = payload)
    if r.text == '0':
        
        print("Error adding data to the server")
    else: # else statement here just to check if data uploaded
        print("Data added")
    time.sleep(0.60) # sleep time needs to change to reflect the 1 min time requirement