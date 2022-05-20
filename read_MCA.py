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
        while(t <= runtime): # add 5 seconds to take into account the time to start
            # reset input buffer
            #ser.reset_input_buffer()
            # readline (or single byte)
            serial_string = ser.readline()
            # translate hex
            #hex_string = binascii.hexlify(serial_string).decode('ascii')
            # save in file
            #temp = int(hex_string,16)
            #textfile.write(hex_string+"\n")
            # print to screen
            #print(int(hex_string,16))
            print(serial_string)
            outputfile.write(serial_string.decode('utf-8'))
            sleep(1)
            t = t + 1

        # stop the run and turn off the source
        ser.write(stop)
        ser.write(check)
        ser.write(dump)
        while (serial_string != dump_read):
            serial_string = ser.readline()
            print(serial_string)
            outputfile.write(serial_string.decode('utf-8'))
        for i in range(256):
            serial_string = ser.readline()
            print(serial_string)
            channelfile.write(serial_string.decode('utf-8'))
        serial_string = ser.readline()
        print('remaining: ', serial_string)
        serial_string = ser.readline()
        print('remaining: ', serial_string)
    except Exception:
        print("Error: cannot read/write")
else:
    print("Error: cannont open port")

# Turn off the source and stop the run


# close text file
outputfile.close()
channelfile.close()
