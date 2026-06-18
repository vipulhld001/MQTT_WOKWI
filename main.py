from umqtt.simple import MQTTClient
from machine import Pin, ADC, time_pulse_us
import network
import ujson
import time

class HCSR04:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
        self.trigger.value(0)

    def distance_cm(self):
        print("Triggering pulse...")
        self.trigger.value(0)
        time.sleep_us(2)
        self.trigger.value(1)
        time.sleep_us(10)
        self.trigger.value(0)

        try:
            duration = time_pulse_us(self.echo, 1, 60000)
            print("Pulse duration:", duration)
            if duration < 0:
                return -1
            distance_cm = duration // 58
            return distance_cm
        except Exception as e:
            print("Error measuring pulse:", e)
            return -1

MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "vipul/sensors"
CLIENT_ID = "vipul_mqtt_client"

RED_LED_TOPIC = "vipul/red"
GREEN_LED_TOPIC = "vipul/green"

red_led = Pin(23, Pin.OUT)
green_led = Pin(22, Pin.OUT)

def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect('Wokwi-GUEST', '')

    for _ in range(30):
        if wifi.isconnected():
            print("WiFi Connected:", wifi.ifconfig())
            return True
        time.sleep(0.5)
    print("WiFi connection failed!")
    return False

def on_message(topic, msg):
    topic = topic.decode()
    msg = msg.decode()
    print(f"Topic: {topic}, Message: {msg}")

    if topic == RED_LED_TOPIC:
        if msg.lower() == "on":
            red_led.value(1)
        elif msg.lower() == "off":
            red_led.value(0)

    elif topic == GREEN_LED_TOPIC:
        if msg.lower() == "on":
            green_led.value(1)
        elif msg.lower() == "off":
            green_led.value(0)

def connect_mqtt():
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=1883)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(RED_LED_TOPIC)
    client.subscribe(GREEN_LED_TOPIC)
    print(f"Connected to MQTT. Subscribed to LED topics {RED_LED_TOPIC} and {GREEN_LED_TOPIC}")
    return client

def main():
    if not connect_wifi():
        print("Failed to connect to WiFi!")
        return

    LDR_PIN = 35
    ldr = ADC(Pin(LDR_PIN))
    ldr.atten(ADC.ATTN_11DB)
    ultra = HCSR04(5, 18)

    try:
        mqtt_client = connect_mqtt()
    except Exception as e:
        print(f"Failed to connect to MQTT: {e}")
        return

    while True:
        try:
            mqtt_client.check_msg()
            ldr_value = ldr.read()
            time.sleep_ms(5)

            distance_cm = ultra.distance_cm()
            time.sleep_ms(5)

            reading = {
                "ldr": ldr_value,
                "proximity_cm": distance_cm,
                "timestamp": time.time()
            }

            payload = ujson.dumps(reading)
            mqtt_client.publish(MQTT_TOPIC, payload)
            print(f"Published: {payload}")

            time.sleep(3)

        except KeyboardInterrupt:
            print("\nShutting down...")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
