# Read data coming from the REM 500 Neutron Survey Meter through a RS-232 serial cable

# Authors: Leo Borrel, Sophie Middleton
# Date: 2022-05-20


import serial
import binascii
from time import sleep

# Set up port
# ser = serial.Serial('/dev/tty.usbserial-AB0K01H7',9600,timeout=100) # Sophie's Macbook
ser = serial.Serial('/dev/ttyUSB0',9600,timeout=100) # Leo's laptop (centos)

ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE


# Create output text files
outputfile = open("count_data.txt","w")
channelfile = open("channel_data.txt","w")

# Check if port is open
try:
    ser.isOpen()
    print("is open")
except:
    print("error: port is close")
    exit()

# Available commands to send
go = 'G'.encode('utf-8') # start the run
stop = 'S'.encode('utf-8') # stop the run
check = 'C'.encode('utf-8') # turn on and off the source in the detector
reset = 'R'.encode('utf-8') # reset data and timer
dump = 'DA'.encode('utf-8') # Dump the data for each channel

dump_read = 'D\r\n'.encode('utf-8') # printed output that separates the count readout from the data dump

# Read/Write
if(ser.isOpen()):
    serial_string = ""
    try:
        # Reset data and start the run
        ser.write(reset)
        ser.write(go)
        ser.write(check)

        # read data for the set runtime
        runtime = 10 # in seconds
        t = 0
        while(t <= runtime):
            # read an entire line of data containing the timestamp and the number of counts in hex format
            serial_string = ser.readline()
            print(serial_string)
            # save the data to the output file
            outputfile.write(serial_string.decode('utf-8'))
            # the REM 500 sends data every second so wait for the new line of data to come
            sleep(1)
            t = t + 1

        # stop the run and turn off the source
        ser.write(stop)
        ser.write(check)
        # dump the channel data
        ser.write(dump)

        # Because the commands sent to the REM 500 are part of the output, usually there is a couple of data lines missing that we need to read now
        # read all the lines until the command to send the data dump is read
        while (serial_string != dump_read):
            serial_string = ser.readline()
            print(serial_string)
            outputfile.write(serial_string.decode('utf-8'))

        # read the data for each one of the 256 channel and save them in the other output file
        for i in range(256):
            serial_string = ser.readline()
            print(serial_string)
            channelfile.write(serial_string.decode('utf-8'))

        # The line right after the channel dump is supposed to be the number of counts with the timestamp
        serial_string = ser.readline()
        print('remaining: ', serial_string)
    except Exception:
        print("Error: cannot read/write")
else:
    print("Error: cannont open port")


# close text file
outputfile.close()
channelfile.close()
