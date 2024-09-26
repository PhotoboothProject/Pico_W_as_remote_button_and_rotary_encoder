# SPDX-FileCopyrightText: 2023 Frank Grootens, Berlin
# SPDX-License-Identifier: MIT 

import os
import time
import ssl
import wifi
import socketpool
import microcontroller
import supervisor
import board
import rotaryio
import digitalio
from digitalio import DigitalInOut, Direction, Pull
import adafruit_requests
from adafruit_debouncer import Button


# Define your Photobooth IP and Hardware Button Server Port
photobooth_ip = "Your_Server_IP"
button_server_port = "Your_Server_Port"    ## Default port is 14711

btn1_pin = DigitalInOut(board.GP10)             ### Connect to GND
btn1_pin.direction = Direction.INPUT
btn1_pin.pull = Pull.UP                         
btn1 = Button(btn1_pin, short_duration_ms=500, long_duration_ms=1000, value_when_pressed=False)

led1 = digitalio.DigitalInOut(board.GP11)       ### Connect to GND
led1.direction = digitalio.Direction.OUTPUT

btn2_pin = DigitalInOut(board.GP12)             ### Connect to GND
btn2_pin.direction = Direction.INPUT
btn2_pin.pull = Pull.UP                         
btn2 = Button(btn2_pin, short_duration_ms=500, long_duration_ms=1000, value_when_pressed=False)

led2 = digitalio.DigitalInOut(board.GP13)       ### Connect to GND 
led2.direction = digitalio.Direction.OUTPUT        

btn3_pin = DigitalInOut(board.GP14)             ### Connect to GND 
btn3_pin.direction = Direction.INPUT            
btn3_pin.pull = Pull.UP                         
btn3 = Button(btn3_pin, short_duration_ms=500, long_duration_ms=1000, value_when_pressed=False)

led3 = digitalio.DigitalInOut(board.GP15)       ### Connect to GND 
led3.direction = digitalio.Direction.OUTPUT    

btn4_pin = DigitalInOut(board.GP16)             ### Connect to GND
btn4_pin.direction = Direction.INPUT
btn4_pin.pull = Pull.UP                       
btn4 = Button(btn4_pin, short_duration_ms=500, long_duration_ms=1000, value_when_pressed=False)

led4 = digitalio.DigitalInOut(board.GP17)       ### Connect to GND
led4.direction = digitalio.Direction.OUTPUT    

btn5_pin = DigitalInOut(board.GP18)             ### Connect to GND
btn5_pin.direction = Direction.INPUT            
btn5_pin.pull = Pull.UP                    
btn5 = Button(btn5_pin, short_duration_ms=500, long_duration_ms=1000, value_when_pressed=False)

led5 = digitalio.DigitalInOut(board.GP19)       ### Connect to GND
led5.direction = digitalio.Direction.OUTPUT

sw_pin = DigitalInOut(board.GP2)                ### Connect to GND
sw_pin.direction = Direction.INPUT
sw_pin.pull = Pull.UP                           
sw = Button(sw_pin, short_duration_ms=500, long_duration_ms=1000, value_when_pressed=False) 

encoder = rotaryio.IncrementalEncoder(board.GP4, board.GP3)
last_position = encoder.position

#  Web requests - URLs that triggers a certain action on the Photobooth Remote Server 
picture_url = f"http://{photobooth_ip}:{button_server_port}/commands/start-picture"         ####   Specify your Photobooth IP and Hardware Button Server Port   ####
collage_url = f"http://{photobooth_ip}:{button_server_port}/commands/start-collage"         ####   Specify your Photobooth IP and Hardware Button Server Port   ####
print_url = f"http://{photobooth_ip}:{button_server_port}/commands/start-print"             ####   Specify your Photobooth IP and Hardware Button Server Port   ####
video_url = f"http://{photobooth_ip}:{button_server_port}/commands/start-video"             ####   Specify your Photobooth IP and Hardware Button Server Port   ####
custom_url = f"http://{photobooth_ip}:{button_server_port}/commands/start-custom"           ####   Specify your Photobooth IP and Hardware Button Server Port   ####
shutdown_url = f"http://{photobooth_ip}:{button_server_port}/commands/shutdown-now"         ####   Specify your Photobooth IP and Hardware Button Server Port   ####
cw_url = f"http://{photobooth_ip}:{button_server_port}/commands/rotary-cw"                  ####   Specify your Photobooth IP and Hardware Button Server Port   ####
ccw_url = f"http://{photobooth_ip}:{button_server_port}/commands/rotary-ccw"                ####   Specify your Photobooth IP and Hardware Button Server Port   ####
btn_press_url = f"http://{photobooth_ip}:{button_server_port}/commands/rotary-btn-press"    ####   Specify your Photobooth IP and Hardware Button Server Port   ####

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

try:
    # Connect to SSID using your credentials
    wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD')) 
    print("Connected to WiFi...")
    #  prints MAC address to REPL
    print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
    #  prints IP address to REPL
    print("My IP address is", wifi.radio.ipv4_address)
except Exception as e:
    print("Cannot connect to WiFi. Try again 10 seconds...", e)
    time.sleep(10)

def wifi_connect():

    while not wifi.radio.connected:
    
        try: 
            # Connect to SSID using your credentials
            wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
            print("Reconnected to WiFi...")
            #  prints MAC address to REPL
            print("wifi_connect: My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
            #  prints IP address to REPL
            print("My IP address is", wifi.radio.ipv4_address)
            time.sleep(1)         
        except Exception as e:
            print("Cannot connect to WiFi. Try again in 10 seconds...", e)
            time.sleep(10)       
        
try:
    while True:
        btn1.update()
        led1.value = not btn1.value
        btn2.update()
        led2.value = not btn2.value
        btn3.update()
        led3.value = not btn3.value
        btn4.update()
        led4.value = not btn4.value
        btn5.update()
        led5.value = not btn5.value
        sw.update()
        
        try:
            if btn1.short_count:              
                    # Execute the get request to the server
                    response = requests.get(picture_url)
                    # Show server response
                    print("-" * 40)
                    print("Text Response: ", response.text)
                    print("-" * 40)
                    response.close()
                    time.sleep(0.2)

            if btn1.long_press: 
                    # Execute the get request to the server
                    response = requests.get(collage_url)
                    # Show server response
                    print("-" * 40)
                    print("Text Response: ", response.text)
                    print("-" * 40)
                    response.close()
                    time.sleep(0.2)
        
            if btn2.short_count:
                    # Execute the get request to the server
                    response = requests.get(print_url)
                    # Show server response
                    print("-" * 40)
                    print("Text Response: ", response.text)
                    print("-" * 40)
                    response.close()
                    time.sleep(0.2)

            if btn2.long_press:
                    # Execute the get request to the server
                    response = requests.get(print_url)
                    # Show server response
                    print("-" * 40)
                    print("Text Response: ", response.text)
                    print("-" * 40)
                    response.close()
                    time.sleep(0.2)

            if btn3.short_count:
                    # Execute the get request to the server
                    response = requests.get(video_url)
                    # Show server response
                    print("-" * 40)
                    print("Text Response: ", response.text)
                    print("-" * 40)
                    response.close()
                    time.sleep(0.2)

            if btn3.long_press:
                    # Execute the get request to the server
                    response = requests.get(video_url)
                    # Show server response
                    print("-" * 40)
                    print("Text Response: ", response.text)
                    print("-" * 40)
                    response.close()
                    time.sleep(0.2)

            if btn4.short_count:
                    response = requests.get(custum_url)
                    # Show server response
                    print("-" * 40)
                    print("Text Response: ", response.text)
                    print("-" * 40)
                    response.close()
                    time.sleep(0.2)

            if btn4.long_press:
                    # Execute the get request to the server
                    response = requests.get(custum_url)
                    # Show server response
                    print("-" * 40)
                    print("Text Response: ", response.text)
                    print("-" * 40)
                    response.close()
                    time.sleep(0.2)

            if btn5.short_count:
                    # Execute the get request to the server
                    response = requests.get(shutdown_url)
                    # Show server response
                    print("-" * 40)
                    print("Text Response: ", response.text)
                    print("-" * 40)
                    response.close()
                    time.sleep(0.2)

            if btn5.long_press:
                    # Execute the get request to the server
                    response = requests.get(shutdown_url)
                    # Show server response
                    print("-" * 40)
                    print("Text Response: ", response.text)
                    print("-" * 40)
                    response.close()
                    time.sleep(0.2)

            if sw.short_count:
                    # Execute the get request to the server
                    response = requests.get(btn_press_url)
                    # Show server response
                    print("-" * 40)
                    print("Text Response: ", response.text)
                    print("-" * 40)
                    response.close()
                    time.sleep(0.2)
                
            if sw.long_press:
                    # Execute the get request to the server
                    response = requests.get(btn_press_url)
                    # Show server response
                    print("-" * 40)
                    print("Text Response: ", response.text)
                    print("-" * 40)
                    response.close()
                    time.sleep(0.2)
          
            current_position = encoder.position
            position_change = current_position - last_position
        
            if position_change > 0:
                for _ in range(position_change):
                    # Execute the get request to the server
                    response = requests.get(ccw_url)
                    # Show server response
                    print("-" * 40)
                    print("Text Response: ", response.text)
                    print("-" * 40)
                    response.close()
                    time.sleep(0.2)

            elif position_change < 0:
                for _ in range(-position_change):
                    # Execute the get request to the server
                    response = requests.get(cw_url)
                    # Show server response
                    print("-" * 40)
                    print("Text Response: ", response.text)
                    print("-" * 40)
                    response.close()
                    time.sleep(0.2)
              
            last_position = current_position
        
        except Exception as e:
            print("An error occured" ,e)
            time.sleep(2)
            while not wifi.radio.connected:
                print("Not connected to wifi - trying to reconnect")
                wifi_connect()
            while wifi.radio.connected:    
                print("HTTP server down? Restart photobooth application or press F5 to refresh browser. Pico will soft reset in 2 seconds")
                time.sleep(2)
                supervisor.reload()

except Exception as e:
    print("An error occured" ,e)
    print("Pico will hard reset in 10 seconds")
    time.sleep(10)
    micorcontroller.reset()
