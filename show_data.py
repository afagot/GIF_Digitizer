import ROOT
import re
import numpy
import time
import glob
import sys,os
from numpy import mean, sqrt, square, std
import numpy as np
import os
import os
first      = int(os.environ['Dig1'])
last       = int(os.environ['Dig2'])
HVPoint    = int(os.environ['HVPoint'])
TimeWindow = int(os.environ['TimeWindow'])

def rms(x):
    return np.sqrt(x.dot(x)/x.size)

###########################################
# analyzer.py works opening several files
# Next is to develop a array loop onening

#inputFile = "/home/analysis/HVSCAN/002409/HV8/HV8.root"
inputFile=[0 for i in range(17)]
inputFile[1]  = "HVSCAN/002589/HV7/HV7.root"
inputFile[2]  = "HVSCAN/002575/HV2/HV2.root"
inputFile[3]  = "HVSCAN/002575/HV3/HV3.root"
inputFile[4]  = "HVSCAN/002575/HV4/HV4.root"
inputFile[5]  = "HVSCAN/002575/HV5/HV5.root"
inputFile[6]  = "HVSCAN/002575/HV6/HV6.root"
inputFile[7]  = "HVSCAN/002575/HV7/HV7.root"

fIn   = [0 for i in range(16)]
data  = [0 for i in range(16)]
rms   = [0 for i in range(16)]
mean  = [0 for i in range(16)]
pulse = [0 for i in range(16)]

for num in range(1,7):
	fIn[num]  = ROOT.TFile(inputFile[num]) # open ROOT file
 	data[num] = fIn[num].Get("data") # get the data tree
# print num
#print "---------------"
run = HVPoint
time = fIn[1].Get("time") # get the time vector

# Loop over all the events for all channels
#for i in range(0, data[7].GetEntries()+1):
for i in range(first, last):

	data[run].GetEntry(i)

	trgTime    = data[run].trgTime

	pulse[0]  = data[run].pulse_ch0
	pulse[1]  = data[run].pulse_ch1
	pulse[2]  = data[run].pulse_ch2
	pulse[3]  = data[run].pulse_ch3
	pulse[4]  = data[run].pulse_ch4
	pulse[5]  = data[run].pulse_ch5
	pulse[6]  = data[run].pulse_ch6
	pulse[7]  = data[run].pulse_ch7
	pulse[8]  = data[run].pulse_ch8
	pulse[9]  = data[run].pulse_ch9
	pulse[10]  = data[run].pulse_ch10
	pulse[11]  = data[run].pulse_ch11
	pulse[12]  = data[run].pulse_ch12
	pulse[13]  = data[run].pulse_ch13
	pulse[14]  = data[run].pulse_ch14
	pulse[15]  = data[run].pulse_ch15

        evNum      = data[run].evNum
        trgTime    = data[run].trgTime

#	print i, evNum
	# loop over the pulse
	for k in range(0,15):
		mean[k] = np.mean(pulse[k][:100])
#		stdv[k] = np.std(pulse[k][:100])*10.0
#	print std

	for j in range(0, pulse[0].size()):
		b = 0 #Stupid Mexican Solutions
		print j, TimeWindow*time[j]/1024.,
		for k in range(0,15):
			print pulse[k][j]-mean[k],
		print ""
#	rms[6] = np.sqrt(np.mean(np.dot(pulse6,pulse6))/1024.)
#	print " --> " + str(rms[6])
#        rms[6] = np.mean(pulse6)
#	print " --> " + str(rms[6])

for num in range(1,7):
	fIn[run].Close()

#inputFile[1]  = "HVSCAN/ecogasboth2/run1/run1.dqm.root"
#inputFile[2]  = "HVSCAN/ecogasboth2/run2/run2.dqm.root"
#inputFile[3]  = "HVSCAN/ecogasboth2/run3/run3.dqm.root"
#inputFile[4]  = "HVSCAN/ecogasboth2/run4/run4.dqm.root"
#inputFile[5]  = "HVSCAN/ecogasboth2/run5/run5.dqm.root"
#inputFile[6]  = "HVSCAN/ecogasboth2/run6/run6.dqm.root"
