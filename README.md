# REM_500_MCA
Python interface with REM 500 Neutron Survey Meter MCA through RS-232 serial port

## Requirements

- Retrieves data from the REM 500 Neutron Survey Meter in MCA mode through a RS-232 serial connection.

- The REM 500 needs to be in MCA mode before launching the script `read_MCA.py`.


# Step by step use

1. Put the REM 500 Neutron Survey Meter in MCA mode:
- Push the `ON/OFF` button
- Push the `MODE` button
- Push the `RESET` button twice (which correspond to `NEXT` in this menu)
- Push the `ALT` button to access the `MCA` mode


2. Change the runtime or the commands you want to send to the REM 500 directly in the file `read_MCA.py`

3. Run the `read_MCA.py` script (as administrator on linux to access the ttyUSB0 interface): 
> sudo python3 read_MCA.py

4. Two output files are generated:
- `count_data.txt` contains timestamps and the number of counts in hex format
- `channel_data.txt` contains the number of counts in each of the 256 channels

Run the `data_extraction.py` script:
> python3 data_extraction.py

It creates a CSV file from the count_data.txt file containing the timestamps converted in seconds and the number of counts converted from hex format.
It also generates a plot of the number of counts as a function of time from the `count_data.txt` file, and it plots the number of counts in each channel from the `channel_data.txt` file

