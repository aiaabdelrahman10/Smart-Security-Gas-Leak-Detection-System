# Smart Security & Gas Leak Detection System

## Overview

This project is an IoT-based Smart Security & Gas Leak Detection System developed using ESP32 and simulated on Wokwi. It integrates motion detection and gas leak monitoring using MQTT communication, enabling real-time monitoring and remote control through a Node-RED dashboard.

## Features

- Motion detection using a PIR sensor.
- Gas leak detection using an MQ2 gas sensor.
- MQTT-based communication using HiveMQ Broker.
- Remote ARM/DISARM control through the Node-RED dashboard.
- LED and Buzzer alerts for security and gas leak events.
- Wi-Fi connectivity using ESP32.
- Real-time monitoring and remote system management.

## Technologies Used

- ESP32
- MicroPython
- Wokwi Simulator
- MQTT
- HiveMQ
- Node-RED

## Project Structure

```
├── main.py
├── diagram.json
├── wokwi-project.txt
└── Smart Security & Gas Leak Detection System Presentation.pptx
```

## System Workflow

### Smart Security System
- Detects motion using a PIR sensor.
- Publishes motion events via MQTT.
- Receives ARM/DISARM commands from the Node-RED dashboard.
- Activates LED and Buzzer only when the system is armed.

### Gas Leak Detection System
- Reads gas concentration using the MQ2 sensor.
- Publishes gas values through MQTT.
- Triggers an alarm when the gas level exceeds the predefined threshold.
- Supports remote monitoring and alarm management.

## Dashboard

*(Insert Node-RED Dashboard screenshot here)*

## Wokwi Simulation

*(Insert Wokwi circuit screenshot here)*

## Future Improvements

- Mobile application integration.
- Cloud database connectivity.
- Email and SMS notifications.
- Event logging and history tracking.
- AI-based anomaly detection.

## Team

**Aya Abdelrahman**
**Neama Hamed**
**Eman Gamil**
**Rana Samir**
