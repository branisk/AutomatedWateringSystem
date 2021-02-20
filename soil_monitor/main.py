import machine
from machine import I2C, Pin, ADC, deepsleep
from time import sleep
#   Obtained from micropython repository
import ssd1306
#   Import espnow
import network
from esp import espnow

#   Define pins for ESP32-WROOM32 Devkit
SCK_PIN = 21
SDA_PIN = 22
AIN_PIN = 36
BAT_PIN = 35

#   Define oled screen dimensions and display
screen_x = 128
screen_y = 32
#i2c = I2C(-1, Pin(SCK_PIN), Pin(SDA_PIN))
#display = ssd1306.SSD1306_I2C(screen_x, screen_y, i2c)

#   Define moisture calibration boundaries
MOISTURE_FLOOR = 1479
MOISTURE_CEIL = 3443

def main():
    wlan = initialize_network()

    esp = espnow.ESPNow()
    sleep(1)
    esp.init()
    sleep(1)
    peer_mc = b'\x10R\x1c^*\xbc'
    esp.add_peer(peer_mc)

    while True:
        #moisture = display_soil_moisture() + "%"
        moisture = get_soil_moisture() + "%"
        voltage = str(get_battery_voltage()) + "V"
        sleep(3)
        esp.send(moisture + " " + voltage)
        deepsleep(3_600_000)    # 60 minutes

def get_soil_moisture():
    soil_moisture = ADC(Pin(AIN_PIN));
    soil_moisture.atten(soil_moisture.ATTN_11DB)
    final_moisture = moisture_to_percent(soil_moisture.read())
    return str(int(final_moisture))

def display_soil_moisture():
    display.fill(0)
    display.text("Soil moisture: ", 1, 1, 1)
    soil_moisture = ADC(Pin(AIN_PIN));
    soil_moisture.atten(soil_moisture.ATTN_11DB)
    final_moisture = moisture_to_percent(soil_moisture.read())
    display.text(str(int(final_moisture)) + "%", 16, 16, 1)
    display.show()
    return str(int(final_moisture))

def initialize_network():
    wlan = network.WLAN()
    wlan.active(True)
    wlan.config(protocol=network.MODE_LR)
    return wlan

def moisture_to_percent(soil_moisture):
    num =  100 - (((soil_moisture - MOISTURE_FLOOR) / (MOISTURE_CEIL - MOISTURE_FLOOR)) * 100)
    if (num > 99):
        return 100
    elif (num < 1):
        return 0
    else:
        return num

def get_battery_voltage():
    vbat = 0.0
    vbat = ADC(Pin(BAT_PIN))
    vbat = vbat.read()
    vbat *= 2.0
    vbat *= 3.3
    return (vbat / 10240)

if __name__ == "__main__":
    main()
