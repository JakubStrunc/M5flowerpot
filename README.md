# M5FlowerPot

M5FlowerPot is a smart plant monitoring system developed in **2023** as part of the **Basics of IoT** course. The project leverages IoT technologies to track environmental conditions of potted plants, ensuring optimal care through real-time monitoring and alerts.

## Project Description
This project integrates sensors and IoT components to measure and display plant conditions. The system collects soil moisture and temperature data, processes it on an M5Stack device, and transmits it to a remote dashboard for visualization and analysis.

## Images
![image](https://github.com/JakubStrunc/M5flowerpot/assets/105900658/2f48d5bd-e4ca-4689-820b-b93ba1e32083)
![image](https://github.com/JakubStrunc/M5flowerpot/assets/105900658/a3277320-f843-4e4f-b01e-08d642f5b5a1)
![image](https://github.com/JakubStrunc/M5flowerpot/assets/105900658/bf1c6dc2-058b-4623-9491-d4d7749730ca)
![image](https://github.com/JakubStrunc/M5flowerpot/assets/105900658/037ca062-6367-4fc3-bf52-f3f623124705)

## Devices & Components Used
- **M5Stack Core2** - Main processing unit with display
- **Moisture Sensor and Pump** - Measures soil hydration levels and enables automatic watering
- **ENV II Sensor** - Captures environmental data, including temperature and humidity
- **Wi-Fi Connectivity** - Enables remote data transmission

## Software & Tools Used
- **Visual Studio Code** - Development and programming of M5Stack
- **Mosquitto MQTT Broker** - Message passing between devices
- **Node-RED** - Visual interface for data visualization and automation


## Installation & Setup
### Hardware Setup
1. **Connect the Sensors**:
   - Insert the soil moisture sensor into the plant pot.
   - Attach the ENV II sensor to the M5Stack Core2 using **I2C (SDA: G21, SCL: G22)**.
   - Connect the pump to the **GPIO pin G26** for control.
2. **Power the Device**:
   - Use a USB-C cable to power and program the M5Stack Core2.
   - Ensure the pump has a sufficient power source.

### Software & Network Setup
1. **Clone this repository**:
   ```sh
   git clone https://github.com/JakubStrunc/M5flowerpot.git
   ```
2. **Open the project in Arduino IDE** and install the required libraries:
   - `M5Stack`
   - `ArduinoJson`
   - `WiFi`
   - `PubSubClient` (for MQTT)
3. **Configure the MQTT broker settings**.
4. **Set up Mosquitto MQTT Broker**:
   - Install Mosquitto and configure it for local or cloud-based use.
   - Ensure the M5Stack device is correctly publishing and subscribing to MQTT topics.
5. **Configure Node-RED**:
   - Import the provided Node-RED flow.
   - Ensure the flow receives data from MQTT.
6. **Upload the code to the M5Stack device** and ensure it communicates properly with the MQTT broker and Node-RED.







