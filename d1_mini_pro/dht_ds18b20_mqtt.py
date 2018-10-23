import time
import machine
import onewire
import ds18x20
from umqtt.simple import MQTTClient
import dht

d = dht.DHT11(machine.Pin(13))


def readDHT():
    d.measure()
    t = d.temperature()
    h = d.humidity()
    return (t, h)


client = MQTTClient("mqtt_client_id", "broker server ip address", port=1883)
client.connect()
# the device is on GPIO12
dat = machine.Pin(12)

# create the onewire object
ds = ds18x20.DS18X20(onewire.OneWire(dat))

# scan for devices on the bus
roms = ds.scan()
print('found devices:', roms)

# loop 10 times and print all temperatures
while True:
    time.sleep_ms(10000)
    print('temperatures:', end=' ')
    ds.convert_temp()
    dhtt, hum = readDHT()
    for rom in roms:
        temp = str(ds.read_temp(rom))
        json_temp = '{"ds18b20":{"temperature": "'+str(
            temp)+'"}, "dht11":{"temperature": "'+str(dhtt)+'", "humidity": "'+str(hum)+'"}}'
        client.publish(topic="KevinFan/lab305/temp_hum", msg=json_temp)
        print(ds.read_temp(rom), end=' ')
    print()
