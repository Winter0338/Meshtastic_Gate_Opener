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
                uart.write("Message Recieved! Opening...")
            except:
                pass
