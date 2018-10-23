def connectAP(ssid, pwd):
    import network
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        wlan.active(True)
        wlan.connect(ssid, pwd)

        while not wlan.isconnected():
            pass

    print('network config: ', wlan.ifconfig())
