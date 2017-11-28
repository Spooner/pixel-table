# Pixel-Table

Pixel table development


## Simulator/monitor/controller

Console app.

## Requirements
    
    sudo apt install python-numpy python-pillow python-smbus 
    sudo apt install libffi-dev libssl-dev
    sudo apt install arduino-core arduino-mk
    sudo apt install scons
    
    git clone https://github.com/jgarff/rpi_ws281x.git
    cd rpi_ws281x
    scons
    
    sudo pip install -r requirements.txt


## Flashing the microcontroller

    cd sketchbook/arduino
    make
    make upload
    
    
## Ensure something???
 
    sudo modprobe i2c_bcm2708
    
    
## Run

Test on PC:

    GPIOZERO_PIN_FACTORY=mock ./pixel-table.py console