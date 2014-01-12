import time
import spidev


# SPI connection
SCE  = 10 # gpio pin 24 = wiringpi no. 10 (CE0 BCM 8)
SCLK = 14 # gpio pin 23 = wiringpi no. 14 (SCLK BCM 11)
DIN  = 12 # gpio pin 19 = wiringpi no. 12 (MOSI BCM 10)

# data
COLS = 20
ROWS = 4

# commands
VFD_CLEARDISPLAY = 0x01
VFD_RETURNHOME = 0x02
VFD_ENTRYMODESET = 0x04
VFD_DISPLAYCONTROL = 0x08
VFD_CURSORSHIFT = 0x10
VFD_FUNCTIONSET = 0x20
VFD_SETCGRAMADDR = 0x40
VFD_SETDDRAMADDR = 0x80

# flags for display entry mode
VFD_ENTRYRIGHT = 0x00
VFD_ENTRYLEFT = 0x02
VFD_ENTRYSHIFTINCREMENT = 0x01
VFD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
VFD_DISPLAYON = 0x04
#VFD_DISPLAYOFF = 0x00
VFD_CURSORON = 0x02
VFD_CURSOROFF = 0x00
VFD_BLINKON = 0x01
VFD_BLINKOFF = 0x00

# flags for display/cursor shift
VFD_DISPLAYMOVE = 0x08
VFD_CURSORMOVE = 0x00
VFD_MOVERIGHT = 0x04
VFD_MOVELEFT = 0x00

# flags for function set
VFD_8BITMODE = 0x10
VFD_4BITMODE = 0x00
VFD_2LINE = 0x08
VFD_1LINE = 0x00
VFD_BRIGHTNESS25 = 0x03
VFD_BRIGHTNESS50 = 0x02
VFD_BRIGHTNESS75 = 0x01
VFD_BRIGHTNESS100 = 0x00

VFD_5x10DOTS = 0x04
VFD_5x8DOTS = 0x00

VFD_SPICOMMAND = 0xF8
VFD_SPIDATA = 0xFA


def init():
    _displayfunction = VFD_8BITMODE
    begin(COLS,ROWS,_displayfunction, VFD_BRIGHTNESS25)

def begin(cols, lines, _displayfunction, brightness):
#    if lines > 1:
#       _displayfunction |= VFD_2LINE

    setBrightness(_displayfunction, brightness)

    _numlines = lines
    _currline = 0
    
    # Initialize to default text direction (for romance languages#include "SPI_VFD.h"
    _displaymode = VFD_ENTRYLEFT | VFD_ENTRYSHIFTDECREMENT 
    # set the entry mode
    command(VFD_ENTRYMODESET | _displaymode) 

    # go to address 0
    command(VFD_SETDDRAMADDR)  
    
    # turn the display on with no cursor or blinking default
    command(VFD_DISPLAYCONTROL | VFD_DISPLAYON | VFD_BLINKON)
    
    
    clear()
    home()
    
def display(_displaycontrol): 
    _displaycontrol |= VFD_DISPLAYON 
    command(VFD_DISPLAYCONTROL | _displaycontrol)  
 
def clear():
    command(VFD_CLEARDISPLAY)
    time.sleep(2)

def home():
    command(VFD_RETURNHOME)
    time.sleep(2)

def setBrightness(_displayfunction, brightness):
    #set the brightness (only if a valid value is passed
#    if brightness <= VFD_BRIGHTNESS25: 
#        _displayfunction &= ~VFD_BRIGHTNESS25
#        _displayfunction |= brightness

    command(VFD_FUNCTIONSET | _displayfunction)
    data(brightness)

def setCursor(col, row):
    _numlines = ROWS
    row_offsets = [0x00, 0x40, 0x14, 0x54]
    if row > _numlines:
       row = _numlines-1        # count rows starting with 0
    print ("Sending cursor data :")
    command(VFD_SETDDRAMADDR | (col + row_offsets[row]) )

def noDisplay(vfdoff):
    command(VFD_DISPLAYCONTROL | vfdoff)


def text(string):
    #   display_char(ord(char))
#    l = [VFD_SPIDATA]
    for char in string:
        data(ord(char))
#       l.append(ord(char))
#    spi.writebytes(list(l))
    
def blank_lines():
    thistext = "                    "
    setCursor(0,0)
    text(thistext)
    setCursor(0,1)
    text(thistext)     

def command(_setting):
    spi.xfer2([VFD_SPICOMMAND, _setting])

def data(_byte):
    spi.xfer2([VFD_SPIDATA, _byte])
  

# initalize SPI
spi = spidev.SpiDev()

spi.open(0,0)
spi.max_speed_hz=5000000
# set spi mode to 3WIRE
spi.mode = 3

print("<==== Mainlline Starts ====>")
init()

print("<==== Print Text ====>")
setCursor(0,0)
thistext = "Hello, World!"
text(thistext)


setCursor(0,1)
thistext = "See me Again!"
text(thistext)

time.sleep(4)

blank_lines()
setCursor(0,0)
thistext = "See me now?"
text(thistext)

setCursor(0,1)
thistext = "I'm Back!"
text(thistext)

print("<==== End of Program ====>")

