import machine
from machine import I2C, Pin, ADC, deepsleep
import time
from time import sleep
import network
from esp import espnow

#   Obtained from micropython repository
import ssd1306

#import wifi_module

#   Define pins for ESP32-WROOM32 Devkit
SCK_PIN = 21
SDA_PIN = 22
NUM_MESSENGERS = 2

#   Mac addresses for espnow peers
MAC_AIR_CONTROLLER = b'|\x9e\xbd\xf1{\xd8'
MAC_SOIL_MONITOR = b'\xb8\xf0\t\x95\x99\xac'


def main():
    display = initialize_oled()
    display_values_og(display, 'Initialized.')
    wlan, esp = initialize_network()
    sleep(3)
    index=0

    while True:
        intial_time = time.clock()
        messages = []

        #   Wait to receive all messages
        while (len(messages) < NUM_MESSENGERS):
            messages.append(esp.recv(2100))
            sleep(1)

        for msg in messages:
            mac = msg[0]
            string = msg[1]
            if mac == MAC_AIR_CONTROLLER:
                display_air_values(display, string)
            elif mac == MAC_SOIL_MONITOR:
                display_soil_values(display, string)
            else:
                display_values_og(display, "Mac failure")

        detect_malfunction()
        sleep(900 - (time.clock() - initial_time)) #   15 minutes

def detect_malfunction():
    return

def display_values_og(display, msg):
    display.fill(0)
    display.text(msg, 1, 1, 1)
    display.show()

def display_air_values(display, msg):
    display.fill(0)
    display.text("Temp: " + "RH:" + " CO2:", 1, 1, 1)
    display.text(msg, 10, 16, 1)
    display.show()

def display_soil_moisture(display, msg):
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
    esp = espnow.ESPNow()
    esp.init()
    return wlan, esp

if __name__ == "__main__":
    main()
