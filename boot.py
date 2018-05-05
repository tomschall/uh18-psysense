from network import WLAN
import json
import machine

# read config
with open('config.json') as json_data_file:
    CONFIG = json.load(json_data_file)
print("Used configuration:")
print(CONFIG)

wlan = WLAN(mode=WLAN.STA)
print("Scanning networks...")
nets = wlan.scan()

for net in nets:
    if net.ssid == CONFIG["wlan"]["ssid"]:
        print('Network found!')
        wlan.connect(net.ssid, auth=(
            net.sec, CONFIG["wlan"]["auth"]), timeout=5000)
        while not wlan.isconnected():
            machine.idle()  # save power while waiting
            # print('Waiting...')
        print('WLAN connection succeeded to:  ' + CONFIG["wlan"]["ssid"])
        break
