import network
from umqtt.simple import MQTTClient
from machine import Pin, ADC
import time

# WiFi
SSID = "Wokwi-GUEST"
PASSWORD = ""

# MQTT
MQTT_BROKER = "broker.hivemq.com"
CLIENT_ID = "esp32-combined"

# Motion Sensor Pins
pir = Pin(13, Pin.IN)
motion_led = Pin(18, Pin.OUT)

# MQ2 Sensor
gas = ADC(Pin(34))
gas.atten(ADC.ATTN_11DB)
gas.width(ADC.WIDTH_12BIT)

# Gas LED
gas_led = Pin(4, Pin.OUT)

# Topics
GAS_TOPIC_1 = "gas/value"
GAS_TOPIC_2 = "gas/status"
ALARM_TOPIC = "gas/alarm"

MOTION_TOPIC = "motionsensor/alarm"
MOTION_STATUS_TOPIC = "motionsensor/status"
MOTION_INFO= "motionsensor/info"

# States
armed = False
alarm_enabled = True

# Threshold
THRESHOLD = 2000

# MQTT Callback
def callback(topic, msg):
    global armed
    global alarm_enabled

    topic = topic.decode()
    command = msg.decode().strip().upper()

    print("Received:", command)

    if topic == MOTION_TOPIC:

        if command == "ARM":
            armed = True
            print("System ARMED")

        elif command == "DISARM":
            armed = False
            print("System DISARMED")

    elif topic == ALARM_TOPIC:

        if command == "ON":
            alarm_enabled = True
            print("Alarm Enabled")

        elif command == "OFF":
            alarm_enabled = False
            gas_led.off()
            print("Alarm Disabled")


# Connect WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

print("Connecting WiFi...")

while not wifi.isconnected():
    time.sleep(0.2)

print("WiFi Connected!")

# Connect MQTT
client = MQTTClient(CLIENT_ID, MQTT_BROKER)
client.set_callback(callback)
client.connect()

# Subscribe
client.subscribe(MOTION_TOPIC)
client.subscribe(ALARM_TOPIC)

print("MQTT Connected!")

while True:

    # Check incoming MQTT messages
    client.check_msg()

    # ---------------- Motion System ----------------

    motion = pir.value()

    if armed :
        client.publish(
                 MOTION_INFO,
                 b"SYSTEM ARMED"
            )
        if motion :

            print("Motion Detected!")

        
            motion_led.on()

            client.publish(
                 MOTION_STATUS_TOPIC,
                 b"Motion Detected!"
            )

            time.sleep(2)
        else:
            motion_led.off()
            client.publish(
                 MOTION_STATUS_TOPIC,
                 b"NO Motion Detected!"
            )

    else:
            motion_led.off()
            client.publish(
                 MOTION_INFO,
                 b"SYSTEM DISARMED"
            )
            client.publish(
                 MOTION_STATUS_TOPIC,
                 b"System OFF"
            )
        
        

    # ---------------- Gas System ----------------

    gas_value = gas.read()
    

    print("Gas Value:", gas_value)

    client.publish(GAS_TOPIC_1, str(gas_value))

    if alarm_enabled:

        if gas_value >= THRESHOLD:

            gas_led.on()

            client.publish(
                GAS_TOPIC_2,
                b"GAS LEAK DETECTED"
            )

        else:
            client.publish(
                GAS_TOPIC_2,
                b"SAFE"
            )
            gas_led.off()
    else :
        client.publish(
                GAS_TOPIC_2,
                b"ALARM DISABLED"
            )        

    time.sleep(1)