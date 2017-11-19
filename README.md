# Pixel-Table

Pixel table development


## Simulator/monitor/controller

Console app.

## Requirements

### Client

    sudo apt install xsel
    
### Server
    
    sudo apt install python-numpy python-smbus
    sudo apt install arduino-core arduino-mk
    sudo apt install x11-xserver-utils # For "xset"

## Flashing the microcontroller

    make
    make upload
    
    
## Run
    
Test on PC:

    GPIOZERO_PIN_FACTORY=mock ./pixel-table.py