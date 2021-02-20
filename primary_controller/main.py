import machine
from machine import I2C, Pin, ADC, deepsleep
import time
import network
from esp import espnow

#   Obtained from micropython repository
import ssd1306

#import wifi_module

#   Define pins for ESP32-WROOM32 Devkit
SCK_PIN = 21
SDA_PIN = 22

peer_ac = b'|\x9e\xbd\xf1{\xd8'
peer_sm = b'\xb8\xf0\t\x95\x99\xac'
peer_sm_og = b'\x84\xcc\xa8]\x0e,'


def main():
    display = initialize_oled()
    display_values_og(display, 'Initialized.')
    wlan, esp = initialize_network()
    time.sleep(3)
    index=0

    while True:
        msg = esp.recv(2100)
        if msg:
            mac = msg[0]
            string = msg[1]
            display_values_og(display, string)
            if mac == peer_ac:
                display_values(display, string)
            elif mac == peer_sm:
                display_moisture(display, string)
            else:
                display_values_og(display, "Mac failure")
        #else:
        #    display_values_og(display, str(index))#display_values(display, msg[1])
        index+=1
        detect_malfunction()
        time.sleep(3)

def detect_malfunction():
    return

def display_values_og(display, msg):
    display.fill(0)
    display.text(msg, 1, 1, 1)
    display.show()

def display_values(display, msg):
    display.fill(0)
    display.text("Temp: " + "RH:" + " CO2:", 1, 1, 1)
    display.text(msg, 10, 16, 1)
    display.show()

def display_moisture(display, msg):
    display.fill(0)
    display.text("Moisture: " + " " + "Voltage: ", 1, 1, 1)
    display.text(msg, 10, 16, 1)
    display.show()

def initialize_oled():
    #   Define oled screen dimensions and display
    screen_x = 128
    screen_y = 32
    oled = I2C(-1, Pin(SCK_PIN), Pin(SDA_PIN))
    return ssd1306.SSD1306_I2C(screen_x, screen_y, oled)

def initialize_network():
    wlan = network.WLAN()
    wlan.active(True)
    wlan.config(protocol=network.MODE_LR)
    esp = espnow.ESPNow()
    esp.init()
    return wlan, esp

if __name__ == "__main__":
    main()
