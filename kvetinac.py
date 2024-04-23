from m5stack import *
from m5stack_ui import *
from m5ui import *
from uiflow import *
import wifiCfg
from simple2 import MQTTClient
from easyIO import *

import time
import unit



#2625 sucho - 2575mokro
setScreenColor(0xffffff)
env20 = unit.get(unit.ENV2, (1,3))
Watering0 = unit.get(unit.WATERING, unit.PORTA)

WiFiSSID = "zpikiv"; WiFiPassword = "78086975"

label = M5Label("",160,40)
label.set_text_font(FONT_MONT_14)

label.set_text("Connecting Wi-Fi...")
wifiCfg.doConnect(WiFiSSID, WiFiPassword)
label.set_text("Wi-Fi connected.")
wait(1)
label.set_text("")



moisture = None
temperature = None
humidity = None
pressure = None
# water = 0

txtDeg = None
txtTemp = None
txtPress = None
txtMoist = None
txtHum = None

mode = 0
# mode_w = 0


def Screen_set(warning):
  global txtTemp, txtPress, txtHum, txtMoist, txtDeg
  if warning:
    setScreenColor(0xffffff)
    imgTemp = M5Img("res/temp64 (3).png",74, 42,parent=None)
    imgPlant = M5Img("res/pot64 (1).png",74, 144,parent=None)
    imgHum = M5Img("res/humidity (1).png",165, 42,parent=None)
    imgPress = M5Img("res/meter (1).png",165, 152,parent=None)
    txtDeg = M5TextBox(90, 42, "o", lcd.FONT_Default, 0x000000, rotate=0)
    txtTemp = M5TextBox(32, 75, "-", lcd.FONT_DejaVu18, 0x000000, rotate=0)
    txtPress = M5TextBox(235, 165, "-", lcd.FONT_DejaVu18, 0x000000, rotate=0)
    txtMoist = M5TextBox(32, 165, "-", lcd.FONT_DejaVu18, 0x000000, rotate=0)
    txtHum = M5TextBox(244, 75, "-", lcd.FONT_DejaVu18, 0x000000, rotate=0)
    line1 = M5Line(0,120,320,115,0x00ff00,5)
    line2 = M5Line(160,0,160,240,0x00ff00,5)
    
  else:
    setScreenColor(0xffffff)
    imgTemp = M5Img("res/temp64 (3).png",74, 42,parent=None)
    imgPlant = M5Img("res/pot64 (1).png",74, 144,parent=None)
    imgHum = M5Img("res/humidity (1).png",165, 42,parent=None)
    imgPress = M5Img("res/meter (1).png",165, 152,parent=None)
    imgWarn = M5Img("res/warning-24 (2).png",65, 200,parent=None)
    txtDeg = M5TextBox(90, 42, "o", lcd.FONT_Default, 0x000000, rotate=0)
    txtTemp = M5TextBox(32, 75, "-", lcd.FONT_DejaVu18, 0x000000, rotate=0)
    txtPress = M5TextBox(235, 165, "-", lcd.FONT_DejaVu18, 0x000000, rotate=0)
    txtMoist = M5TextBox(32, 165, "-", lcd.FONT_DejaVu18, 0xFF0000, rotate=0)
    txtHum = M5TextBox(244, 75, "-", lcd.FONT_DejaVu18, 0x000000, rotate=0)
    line1 = M5Line(0,120,320,115,0x00ff00,5)
    line2 = M5Line(160,0,160,240,0x00ff00,5)
  


# Describe this function...
def readSensors():
  global moisture, temperature, humidity, pressure
  moisture = round(Watering0.get_adc_value())
  temperature = round(env20.temperature)
  humidity = round(env20.humidity)
  pressure = round(env20.pressure)

# Describe this function...
def updateDisplay():
  global moisture, temperature, humidity, pressure, txtTemp, txtPress, txtHum, txtMoist, mode
  txtTemp.setText(str((str(temperature) + str('C'))))
  txtPress.setText(str((str(pressure) + str('Pa'))))
  txtHum.setText(str((str(humidity) + str('%'))))
  txtMoist.setText(str((str(-2*(moisture - 2625)) + str('%'))))
  if -2*(moisture - 2625) < 20 and mode == 1:
    Screen_set(False)
    mode = 0
    Watering0.set_pump_status(1)
  elif -2*(moisture - 2625) >= 20 and mode == 0:
    Screen_set(True)
    mode = 1
    Watering0.set_pump_status(0)
  

# Describe this function...
def dataPublish():
  global moisture, temperature, humidity, pressure
  client.publish("jstrunc/device1/stat/temperature", str(temperature) ,retain=True)
  client.publish("jstrunc/device1/stat/pressure", str(pressure) ,retain=True)
  client.publish("jstrunc/device1/stat/humidity", str(humidity) ,retain=True)
  client.publish("jstrunc/device1/stat/moisture", str(-2*(moisture - 2625)) ,retain=True)
  # client.publish("jstrunc/device1/stat/tank", str(water) ,retain=True)
  

def buttonA_wasReleased():
  global moisture, temperature, humidity, pressure
  Watering0.set_pump_status(0)
  pass
btnA.wasReleased(buttonA_wasReleased)


def buttonA_wasPressed():
  global moisture, temperature, humidity, pressure
  Watering0.set_pump_status(1)
  pass
btnA.wasPressed(buttonA_wasPressed)

def subs_cbs(topic, msg, retain, dup):
 
  topic = topic.decode("utf-8")
  msg = msg.decode("utf-8")
  if topic == "jstrunc/device1/cmnd/watering":
    if msg == "ON":
      Watering0.set_pump_status(1)
      wait(5)
      # water += 5
      Watering0.set_pump_status(0)
      client.publish("jstrunc/device1/stat/watering", "OFF" ,retain=True)
      
    
      
    


client = MQTTClient("JStruncM5", "test.mosquitto.org", keepalive=600)
client.connect()

client.set_callback(subs_cbs)
client.set_last_will("jstrunc/device1/stat/availability", "offline", retain=True)


client.subscribe("jstrunc/device1/cmnd/temperature")
client.subscribe("jstrunc/device1/cmnd/pressure")
client.subscribe("jstrunc/device1/cmnd/humidity")
client.subscribe("jstrunc/device1/cmnd/moisture")
client.subscribe("jstrunc/device1/cmnd/watering")
# client.subscribe("jstrunc/device1/cmnd/tank")

client.publish("jstrunc/device1/stat/availability", "online",retain=True)


Screen_set(True)

while True:
  readSensors()
  updateDisplay()
  dataPublish()
  client.check_msg()
  wait(2)
  wait_ms(2)












