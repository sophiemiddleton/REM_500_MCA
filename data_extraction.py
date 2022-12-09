# Extraction and plotting of the data taken from the REM 500 Neutron Survey Meter

# Authors: Leo Borrel, Sophie Middleton
# Date: 2022-05-20, edits by Sophie
# python data_extraction.py --run 5 --subrun 0 --date 2022-12-08 --voltage 120

import matplotlib.pyplot as plt
import csv
import argparse
import numpy as np
parser = argparse.ArgumentParser()
parser.add_argument("--run", help="run number")
parser.add_argument("--subrun", help="subrun number")
parser.add_argument("--date", help="date")
parser.add_argument("--voltage", help="voltage")
args = parser.parse_args()

time = []
counts = []

folder = "data/"+str(args.date)+"/run"+str(args.run)+"_"+str(args.subrun)+"/"

with open(folder + "count_data.txt") as data_file:
    for line in data_file:
        if len(line) == 16:
            value = int(line[0:6],16)
            date = line[7:15]
            time.append(int(date[6:8]) + 60*int(date[3:5]) + 3600*int(date[0:2]))
            counts.append(value)

# Plot of the data from each channel
channel = []
with open(folder + "channel_data.txt") as channel_file:
    for line in channel_file:
        channel.append(int(line[0:5]))

QF = []
with open('data/QF.txt') as QF_file:
    for line in QF_file:
        QF.append(float(line[0:-1]))

rad = 0
for i in range(5,255):
    rad += 100 * i * channel[i] / 20

rem = 0
for i in range(5,255):
    rem += 100 * i * channel[i] * QF[i] / 20
# plot
plt.figure()
plt.bar(range(256),channel)

plt.xlabel('channel #')
plt.ylabel('count')

# Export data to csv
csv_file = open(folder + "count_data.csv", 'w')
header = ['time', 'counts']

rows = zip(time, counts)

with open(folder + "count_data.csv", 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)

# plots
plt.figure()
plt.plot(time, counts, 'r--', label=str(args.date)+" "+" Run "+str(args.run)+" Sub run "+str(args.subrun)+" ("+str(args.voltage)+" kV)" )
plt.legend(fontsize=8)
plt.xlabel('time [s]')
plt.ylabel('Counts')

# divide by runtime (in seconds) because the formula works for 1 sec integration
rad_per_hr = rad / time[-1]
rem_per_hr = rem / time[-1]

print('rad: ', rad_per_hr, ' urad/h')
print('rem: ', rem_per_hr, ' urem/h')

# multiply by runtime (in hour)
rad = rad * (time[-1] / 3600)
rem = rem * (time[-1] / 3600)

print('rad: ', rad, ' urad')
print('rem: ', rem, ' urem')

plt.text(400,10000, str(np.round(rad_per_hr,2))+' urad/h', fontsize=12)
plt.text(400,5000, str(np.round(rem_per_hr,2))+' urem/h', fontsize=12)
plt.savefig(str(args.date)+"Run"+str(args.run)+"SubRun"+str(args.subrun)+"("+str(args.voltage)+"kV).pdf")
plt.show()
