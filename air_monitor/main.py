import machine
from machine import I2C, Pin, ADC
import time
from time import sleep
#   Obtained from micropython repository
import ssd1306
import bme280_float as bme280
import CCS811 as ccs811
#import wifi_module
import network
from esp import espnow
import ubinascii

#   Define pins for ESP32-WROOM32 Devkit
SCK_PIN = 21
SDA_PIN = 22

def main():
    index = 0
    wlan = initialize_network()
    #peer_mc = '10:52:1c:5e:2e:bc'
    #e.add_peer(peer_mc)
    display = initialize_oled()
    bme = initialize_bme()
    ccs = initialize_ccs()

    esp = espnow.ESPNow()
    sleep(1)
    esp.init()
    sleep(1)
    peer_mc = b'\x10R\x1c^*\xbc'
    esp.add_peer(peer_mc)

    while True:
        intial_time = time.clock()
        temp, humidity, pressure, co2, tvoc = calculate_values(bme, ccs)
        display_values(display, temp, humidity, pressure, co2, tvoc)
        time.sleep(3)
        string = str(temp)+ " " + str(humidity) + " " + str(co2)
        esp.send(string)
        deepsleep(900 - (time.clock() - initial_time))  #   15 minutes

def calculate_values(bme, ccs):
    co2 = "-1"
    tvoc = "-1"
    array = bme.values
    temp = int((float(array[0][:-1]) * (9/5))) + 32;
    temp = str(temp) + "F"
    pressure = str(int(float(array[1][:-3]))) + "hPa"
    humidity = str(int(float(array[2][:-1]))) + "%"
    if (ccs.data_ready()):
        co2 = str(ccs.eCO2) + "ppm"
        tvoc = str(ccs.tVOC) + " ppb"
    return temp, humidity, pressure, co2, tvoc

def display_values(display, temp, humidity, pressure, co2, tvoc):
    display.fill(0)
    display.text("Temp: " + "RH:" + " CO2:", 1, 1, 1)
    display.text(temp + " " + humidity + " " + co2, 10, 16, 1)
    display.show()
    return display

def initialize_oled():
    #   Define oled screen dimensions and display
    screen_x = 128
    screen_y = 32
    oled = I2C(-1, Pin(SCK_PIN), Pin(SDA_PIN))
    return ssd1306.SSD1306_I2C(screen_x, screen_y, oled)

def initialize_ccs():
    ccs = I2C(scl=Pin(SCK_PIN), sda=Pin(SDA_PIN))
    return ccs811.CCS811(i2c=ccs, addr=90)

def initialize_bme():
    bme = I2C(scl=Pin(SCK_PIN), sda=Pin(SDA_PIN), freq=10000)
    return bme280.BME280(i2c=bme)

def initialize_network():
    wlan = network.WLAN()
    wlan.active(True)
    return wlan

if __name__ == "__main__":
    main()
