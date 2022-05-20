# REM_500_MCA
Python interface with REM 500 Neutron Survey Meter MCA through RS-232 serial port

## Requirements

- Retrieves data from the REM 500 Neutron Survey Meter in MCA mode through a RS-232 serial connection.

- The REM 500 needs to be in MCA mode before launching the scripts.


## Step by step use

1. Change the runtime or the commands to send to the REM 500 directly in the file `read_MCA.py`

2. Run the read_MCA.py script: 
> python3 read_MCA.py

3. Two output files are generated:
- `count_data.txt` contains timestamps and the number of counts in hex format
- `channel_data.txt` contains the number of counts in each of the 256 channels

4. Run the data_extraction.py script:
> python3 data_extraction.py

It creates a CSV file from the count_data.txt file containing the timestamps converted in seconds and the number of counts converted from hex format.
It also generates a plot of the number of counts as a function of time from the `count_data.txt` file, and it plots the number of counts in each channel from the `channel_data.txt` file

