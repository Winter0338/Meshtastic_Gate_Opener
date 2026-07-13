<img width="755" height="100" alt="ascii-art-text" src="https://github.com/user-attachments/assets/d0e2d607-bdb1-4831-8eb3-a3b1f1ab8cfd" />

_____________________________________________________________________________________________________________________

A simple script and wiring diagram that allows users to construct a Meshtastic LoRa client node capable of opening clicker gates over exceptionally long distances.

### !!! NOTICE !!!

*This is an amateur project. I can almost guarentee that there is a simpler and cheaper way to make a node like this. This is here for anyone looking to create something similar, or improve upon this design. The information I used to create this project [can be found here](https://youtu.be/51Bgt5E5PZg?si=shEbkCdp3YYOjwUT). If you get lost in the following instructions, refer to this info.*

## Parts

* [2x Raspberry Pi Pico](https://www.amazon.com/dp/B08X7HN2VG)
* [1x Waveshare Pico SX1262 LoRa Node Module](https://www.amazon.com/dp/B0F82XK3JC)
* [5V DC Relay](https://www.amazon.com/dp/B095YD3732)
* [Paired Gate Clicker (any one should work however I'm using this one)](https://www.amazon.com/Chamberlain-Replacement-893LM-893Max-1993-Present/dp/B08CNKBTYJ?sr=8-51)

## Instructions

### Step #1

Go to the meshtastic web flasher and flash one of your Pi Picos with the meshtastic firmware. Follow the instructions posted [here](https://flasher.meshtastic.org/) to do so properly. After doing so, you may attatch the Waveshare LoRa hat to the newly flashed pico. 

### Step #2

Connect to your meshtastic flashed pi pico via the [meshtastic web ui](https://client.meshtastic.org/messages/broadcast/0). Create a private channel set under primary. I recommend using a 128 to 256 bit password. After doing so, add any other nodes you want to have access to this channel. 

### Step #3

Flash your second Pi Pico with the micropython firmware. The files and instructions required to do so can be found [here](https://micropython.org/download/RPI_PICO/). 

### Step #4

Download [Thonny](https://thonny.org/) and plug in your micropython flashed pico. Go to Run -> Configure Interpreter... and select MicroPython(Raspberry Pi Pico) from the first drop down menu. On the second drop down menu select the COM port that your pi pico is connected to.

### Step #5

Copy the contents of the main.py file into Thonny and prepare to do some customization. 

```python
from machine import UART, Pin
import time

######################
#PINOUT AND UART INIT#
######################

uart = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9))
relay = Pin(28, Pin.OUT)

##################
#Message Cleaning#
##################

# This function extracts the exact message sent from all the wrapping text around it
def process_uart_message(raw_message):
    """ Function to read from UART, process the message, and return the decoded message as a string. """
    # Locate the start of the message using the ": " delimiter
    colon_space_pos = raw_message.find(b": ")
    
    if colon_space_pos != -1:
        # Extract from the position after ': ' to before the last 2 chars (\r\n)
        extracted_message = raw_message[colon_space_pos + 2:-2]
        try:
            # Decode only the extracted part
            decoded_message = extracted_message.decode('utf-8')
            return decoded_message  # Return the extracted message as a decoded string
        except UnicodeDecodeError:
            error_message = ("Decoding error occurred with the extracted message.")
            return error_message
    else:
        error_message = ("Delimiter ': ' not found in the message.")
        return error_message
        return None

#############
#Relay Logic#
#############

def switch():
    relay.value(1)
    time.sleep(3)
    relay.value(0)
    return None


######
#MAIN#
######

while True:
    if uart.any():
        rawmessage = uart.read()
        message = process_uart_message(rawmessage)

        #Add your own passphrase here. This is the message the pico is looking for to activate the relay. Something like: "open main gate"
        if message.startswith("Your Passphrase Here!"):
            try:
                #optional debugging line  
                print("recieved")
                switch()
                #Confirmation Message, you can change if you'd like
                uart.write("Message Recieved! Opening...")
            except:
                pass
```

In the main section, at the bottom of the code, you must change your passphrase. This is the message the microcontroller is looking for in order to open the gate. I recommend using the name of the gate, so that if you decide to make more nodes, you can keep them all on the same meshtastic channel without opening all of them at once. Something like "entrance gate open" would work. You can also change the confirmation message to whatever you want. After your changes are complete, save the code to the pi pico, making sure the file is named main.py. 

### Step #6

Using the attatched wiring diagram, wire up your two picos accordingly. Some tinkering may be required in order for your relay module to properly set off the clicker, however, you can find what button legs will set off the clicker by bridging the different button legs until the clicker LED blinks. 

<img width="721" height="791" alt="meshtastic_gate_opener_wiring_diagram drawio" src="https://github.com/user-attachments/assets/ad600823-13f4-4316-85d5-4d740c63f966" />

### Step #7 

Clean up and Enjoy! If there is a .stl file in this repo, it is a 3D printed case designed to house these components. 

_____________________________________________________________________________________________________________________

[<img width="82" height="89" alt="0 REAL rating" src="https://github.com/user-attachments/assets/3149d229-34b1-419a-adab-3764423f01f1" />](https://www.realgoodai.org/real-rating)
