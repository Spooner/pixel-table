# Pixel-Table

Pixel table development


## Simulator/monitor/controller

Kivy app (can be run via VNC or potentially as an app).


## Requirements

### Client

    sudo apt install xsel
    
### Server
    
    sudo apt install python-numpy python-smbus
    sudo apt install arduino-core arduino-mk


## Flashing the microcontroller

    make
    make upload
    
    
## Run
    
Test on PC:

    GPIOZERO_PIN_FACTORY=mock ./server.py