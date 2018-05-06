###############################################################################
# uh18-psysense
#
# Send osc signals from several sensors via osc to #shipbeat.
# Use config.json for WLAN and OSC configuration
#
# (c) toadtec 2018
###############################################################################
# include system libs
import time
import json
# include debug libs
import gc
import machine
import micropython

# include pysense libs
from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE
# include osc libs
from uosc.client import Bundle, Client, create_message


# read config
with open('config.json') as json_data_file:
    CONFIG = json.load(json_data_file)

# setup osc
osc = Client(CONFIG["osc"]["server"], CONFIG["osc"]["port"])

py = Pysense()
# Send sensor data forever
while True:
    # Send pressure in Pa
    mpp = MPL3115A2(py, mode=PRESSURE)
    pressureOscData = str(mpp.pressure())
    osc.send(CONFIG["osc"]["sensors"]["pressure"], pressureOscData)
    print("Pressure: " + pressureOscData)

    # Send 3-axis acceleration
    li = LIS2HH12(py)
    accelerationOscData = li.acceleration()

    osc.send(CONFIG["osc"]["sensors"]["accelerationX"], accelerationOscData[0])
    print("Acceleration: " + str(accelerationOscData[0]))

    osc.send(CONFIG["osc"]["sensors"]["accelerationY"], accelerationOscData[1])
    print("Acceleration: " + str(accelerationOscData[1]))

    osc.send(CONFIG["osc"]["sensors"]["accelerationZ"], accelerationOscData[2])
    print("Acceleration: " + str(accelerationOscData[2]))

    # Send light values
    lt = LTR329ALS01(py)
    osc.send(CONFIG["osc"]["sensors"]["lightBlue"], str(lt.light()[0]))
    print("Light (channel Blue lux, channel Red lux): " + str(lt.light()[0]))

    time.sleep_ms(100)
    # print('free:', str(gc.mem_free()))
    # print('info:', str(machine.info()))
    # print('info:', str(gc.mem_alloc()))
    # print('info:', str(micropython.mem_info()))
    gc.collect()

    #########################################
    # Example code
    #########################################
    # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals

    # mp = MPL3115A2(py, mode=ALTITUDE)
    # si = SI7006A20(py)
    # lt = LTR329ALS01(py)
    # li = LIS2HH12(py)

    # print("MPL3115A2 temperature: " + str(mp.temperature()))

    # print("Altitude: " + str(mp.altitude()))

    # print("Temperature: " + str(si.temperature()) +
    # " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")
    # print("Dew point: " + str(si.dew_point()) + " deg C")
    # t_ambient = 24.4
    # print("Humidity Ambient for " + str(t_ambient) +
    # " deg C is " + str(si.humid_ambient(t_ambient)) + "%RH")

    # print("Light (channel Blue lux, channel Red lux): " + str(lt.light()))

    # print("Acceleration: " + str(li.acceleration()))
    # print("Roll: " + str(li.roll()))
    # print("Pitch: " + str(li.pitch()))

    # print("Battery voltage: " + str(py.read_battery_voltage()))

    #
