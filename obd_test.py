import obd

import time

connection = obd.OBD()  # auto-connects to USB or RF port

def obd_speed():
    cmd = obd.commands.SPEED  # select an OBD command (sensor)

    response = connection.query(cmd)  # send the command, and parse the response

    print(response.value)  # returns unit-bearing values thanks to Pint
    print(response.value.to("mph"))  # user-friendly unit conversions

    return response.value.to("mph")

print ("speed = : " + str(obd_speed()))