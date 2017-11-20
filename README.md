# Pixel-Table

Pixel table development


## Simulator/monitor/controller

Console app.

## Requirements
    
    sudo apt install python-numpy python-smbus
    sudo apt install arduino-core arduino-mk
    sudo apt install x11-xserver-utils # For "xset"
    sudo apt install scons
    
    git clone https://github.com/jgarff/rpi_ws281x.git
    cd rpi_ws281x
    scons
    
## Flashing the microcontroller

    make
    make upload
    
    
## Run
    
Test on PC:

    GPIOZERO_PIN_FACTORY=mock ./pixel-table.py