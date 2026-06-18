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

## ⚡ Hardware Wiring Configuration

The code is pre-mapped to the following pins on your ESP32 board or your Wokwi simulation space:

### 1. Sensory Elements (Inputs)
| Component | Device Pin | ESP32 Pin | Mode / Configuration |
| :--- | :---: | :---: | :--- |
| **LDR (Photoresistor)** | Signal Output | **GPIO 35** | Analog input (`ADC.ATTN_11DB` / ~3.3V range) |
| **HC-SR04 Ultrasonic** | Trigger | **GPIO 5** | Digital Output |
| **HC-SR04 Ultrasonic** | Echo | **GPIO 18** | Digital Input |

### 2. Actuators (Outputs)
| Component | Color | ESP32 Pin | Active Value |
| :--- | :---: | :---: | :--- |
| **LED** | Red | **GPIO 23** | `1` (ON) / `0` (OFF) |
| **LED** | Green | **GPIO 22** | `1` (ON) / `0` (OFF) |

---

## 📡 Protocol & Broker Details

- **MQTT Broker Host:** `test.mosquitto.org`
- **Default Port:** `1883` (Unencrypted)
- **Client Identifier:** `vipul_mqtt_client`

### Topic Topology
| Topic Path | Direction | Payload Type | Description |
| :--- | :---: | :--- | :--- |
| **`vipul/sensors`** | **Publish** | `JSON` | Pushes object carrying `ldr`, `proximity_cm`, and `timestamp` every 3 seconds. |
| **`vipul/red`** | **Subscribe**| `String` | Acceptable values: `"on"` or `"off"` to drive the Red LED state. |
| **`vipul/green`**| **Subscribe**| `String` | Acceptable values: `"on"` or `"off"` to drive the Green LED state. |

## 🛠️ Software Requirements

To successfully run this script on an embedded or virtual target:
* Ensure your target board is running a valid version of **MicroPython v1.19+**.
* The core framework depends on the standard `umqtt.simple` package.

If using hardware connected to the open internet, run:
```python
import upip
upip.install('micropython-umqtt.simple')


3. Remote Controlling LEDs
To toggle your onboard physical/virtual connections remotely via an external MQTT client terminal tool (like MQTTX or Mosquitto CLI):

Turn on the Green LED:

Bash
mosquitto_pub -h test.mosquitto.org -t "vipul/green" -m "on"
Turn off the Red LED:

Bash
mosquitto_pub -h test.mosquitto.org -t "vipul/red" -m "off"
