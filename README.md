# MQTT_WOKWI
Connecting MQTT with ESP32 (Based on Mosquitto Broker)
# MicroPython Smart Sensor Node with MQTT Control (ESP32)

An IoT edge application written in **MicroPython** for the **ESP32** microcontroller. This project implements a bidirectional telemetry system using the **MQTT** protocol. It reads environmental values from a Photoresistor (LDR) and an Ultrasonic Sensor (HC-SR04), publishes JSON telemetry to a broker, and acts on incoming subscription messages to toggle remote LEDs.

---

## 📊 System Architecture

```text
       +--------------------------------------------+
       |                ESP32 Node                  |
       |                                            |
       |  [LDR (ADC 35)]     [HC-SR04 (5, 18)]      |
       |        |                    |              |
       |        v                    v              |
       |   +------------------------------------+   |
       |   | MicroPython Firmware (main.py)     |   |
       |   +------------------------------------+   |
       |        |                    ^              |
       |        v (Publish Payload)  | (Subscribe)  |
       |  [LED Red (23)]     [LED Green (22)]       |
       +--------|--------------------|--------------+
                |                    |
  MQTT Topic:   |                    | MQTT Topics:
  "vipul/sensors"                    | "vipul/red" & "vipul/green"
                v                    |
       +--------------------------------------------+
       |           Public MQTT Broker               |
       |         (test.mosquitto.org)               |
       +--------------------------------------------+

