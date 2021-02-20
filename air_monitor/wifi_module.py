import network

class wifi_module:

def connect_to_wifi():
    SSID = '2Gee'
    KEY = 'livelywhale837'

    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)

    sta_if.active()
    ap_if.active()
    sta_if.connect(ssid, key)

    if (sta_if.isconnected())
        print("Connected to wifi")
