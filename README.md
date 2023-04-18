# Automated Watering System

This repository contains the code for an Automated Watering System, designed to monitor and maintain soil moisture levels for plants. The system is built using MicroPython and integrates multiple sensors, including CCS811, BME280, and SSD1306.

## Sensor Descriptions
- **CCS811**: This sensor measures air quality by detecting volatile organic compounds (VOCs) and equivalent CO2 (eCO2) levels.
- **BME280**: This sensor measures temperature, humidity, and atmospheric pressure.
- **SSD1306**: This is an OLED display module used for displaying the sensor data and system status.

The Python scripts for each sensor are located in the root directory of the repository.

## Controllers

The Automated Watering System consists of three main controllers:

    1. Main Controller (main_controller/main.py): This is the primary script that runs the entire system. It initializes the sensors and controllers, and manages the scheduling of sensor readings and watering actions.

    2. Soil Monitor Controller (soil_monitor_controller/soil_monitor.py): This script manages the soil moisture sensor and determines when the plants need watering. It sends a signal to the main controller to activate the watering system when required.

    3. Air Monitor Controller (air_monitor_controller/air_monitor.py): This script monitors air quality, temperature, and humidity using the CCS811 and BME280 sensors. The data collected is displayed on the SSD1306 OLED display.

## Setup and Usage

To set up the Automated Watering System, follow these steps:

    1. Clone this repository to your local machine.
    2. Ensure that you have the necessary hardware components and connect them according to the system design.
    3. Upload the MicroPython firmware to your microcontrollers (if not already installed).
    4. Upload the main controller, soil monitor controller, air monitor controller, and sensor scripts to your microcontrollers.
    5. Adjust any settings or parameters in the scripts as necessary for your specific hardware or application.
    6. Reset your microcontroller to start running the Automated Watering System.

Please refer to the documentation for each sensor and your specific microcontroller for more detailed instructions on setup and usage.
