# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
import gc
from connect import connectAP
connectAP('ssid', 'password')
import webrepl
webrepl.start()
gc.collect()

import dht_ds18b20_mqtt
