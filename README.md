# Pixel-Table

Pixel table development


## Simulator/monitor/controller

Console app.

## Requirements
    
    sudo apt install -y python-numpy python-pillow python-smbus
    sudo apt install -y libffi-dev libssl-dev
    sudo apt install -y arduino-core arduino-mk scons
    
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

Run on Pi running full-sized Pixel Table:

    ./pixel-table.py neo_pixels
    
Run on Pi with UnicornHatHD:

    ./pixel-table.py unicorn

Test on PC:

    GPIOZERO_PIN_FACTORY=mock ./pixel-table.py console