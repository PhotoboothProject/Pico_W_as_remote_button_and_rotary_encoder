# Raspberry Pi Pico W as HTTP client: Use of Hardware Buttons and Rotary Encoder

Raspberry Pi Pico W CiruitPython code for using the Pico W as a HTTP client in the [Photobooth Project](https://photoboothproject.github.io). You can connect several Buttons or a Rotary Encoder to trigger different actions.

## Requirements:

- Download and install  CircuitPython as described [here](https://learn.adafruit.com/pico-w-wifi-with-circuitpython/installing-circuitpython)

## Preparation

1. Download and run the automated downloader to get needed files and libraries for your device.

The downloader also asks for your WiFi credentials to create the 
`settings.toml` file for you, also the Remotebuzzer Server IP and Port must be entered if asked to update the `code.py` automatically for you.

```sh
wget -O download-files.sh https://raw.githubusercontent.com/PhotoboothProject/Pico_W_as_remote_button_and_rotary_encoder/main/download-files.sh
bash download-files.sh
```

After running the script, the directory will be structured like this:

```
Photobooth_Pi_Pico_W_HTTP_client/
├── code.py
├── lib/
│   ├── adafruit_connection_manager.mpy
│   ├── adafruit_debouncer.mpy
│   ├── adafruit_requests.mpy
│   └── adafruit_ticks.mpy
├── library_info.txt
└── settings.toml
```

2. Copy the `settings.toml`, `code.py` and `lib` folder to the Pico´s CIRCUITPY folder.

3. Have fun!

## Button actions & LED

Up to 5 buttons can be used which trigger up to 6 different web requests for:
- start-picture
- start-collage
- start-custom
- start-print
- start-video
- shutdown-now

as descirbed in the [Photobooth documentation](https://photoboothproject.github.io/FAQ#can-i-use-hardware-button-to-take-a-picture).

There is also LED support for arcarde push buttons, meaning if you use a combined LED button, triggering the button will also light up the LED.

### Wiring layout

| Button Number | GP Number | LED GP Number | Short Press Action        | Long Press Action         |
|---------------|-----------|---------------|---------------------------|---------------------------|
| 1             | GP10      | GP11          | Trigger Picture           | Trigger Collage           |
| 2             | GP12      | GP13          | Trigger Print             | Trigger Print             |
| 3             | GP14      | GP15          | Trigger Video Capture     | Trigger Video Capture     |
| 4             | GP16      | GP17          | Trigger Custom Capture    | Trigger Custom Capture    |
| 5             | GP18      | GP19          | Trigger Shutdown          | Trigger Shutdown          |

## Rotary encoder

A rotary encoder is implemented: It triggers web requests for cw (clockwise) and ccw (counter-clockwise). Pressing the encoder´s push button will trigger a web request for rotary-btn-press. 

Button 1 (btn1 on GPIO 10) will do two different actions depending on short or long press: A short press will trigger the web request for taking a picture, a long press will trigger the web request for taking a collage. 
