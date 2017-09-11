#!/usr/bin/env python
# Estimate Cluster Size from Rome-Chamber 1.4 mm using Digitizer 16 Channels
# Debug 1 : print 0 if strip not above 10*RMS and Amplitude value if if above 10*RMS
# Debug 2 : Same but with 10*RMS after each strip in parenthesis
# Debug 3 : Will print as debug=1 plus Amplitud Information
# Author Salvador Carrillo Aug/2017 @CERN
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

def rms(x):
    return np.sqrt(x.dot(x)/x.size)


debug    = int(os.environ['DigiCodeDebug'])
first    = int(os.environ['DigiCodeFirst'])
last     = int(os.environ['DigiCodeLast'])
#HVPoint  = int(os.environ['HVPoint'])

NumFiles   = 6

###########################################
# analyzer.py works opening several files
# Next is to develop a array loop onening

#inputFile = "/home/analysis/HVSCAN/002409/HV8/HV8.root"
inputFile=[0 for i in range(16)]

inputFile[1]  = "HVSCAN/ecogasboth2/run1/run1.root"
inputFile[2]  = "HVSCAN/ecogasboth2/run2/run2.root"
inputFile[3]  = "HVSCAN/ecogasboth2/run3/run3.root"
inputFile[4]  = "HVSCAN/ecogasboth2/run4/run4.root"
inputFile[5]  = "HVSCAN/ecogasboth2/run5/run5.root"
inputFile[6]  = "HVSCAN/ecogasboth2/run6/run6.root"

#inputFile[1]  = "HVSCAN/002398/HV1/HV1.root"
#inputFile[2]  = "HVSCAN/002398/HV2/HV2.root"
#inputFile[3]  = "HVSCAN/002398/HV3/HV3.root"
#inputFile[4]  = "HVSCAN/002398/HV4/HV4.root"
#inputFile[5]  = "HVSCAN/002398/HV5/HV5.root"
#inputFile[6]  = "HVSCAN/002398/HV6/HV6.root"
#inputFile[7]  = "HVSCAN/002398/HV7/HV7.root"
#inputFile[8]  = "HVSCAN/002398/HV8/HV8.root"
#inputFile[9]  = "HVSCAN/002398/HV9/HV9.root"


fIn   = [0 for i in range(16)]
data  = [0 for i in range(16)]
rms   = [0 for i in range(16)]
stdv  = [0 for i in range(16)]
mean  = [0 for i in range(16)]
pulse = [0 for i in range(16)]
high  = [0 for i in range(16)]
low   = [0 for i in range(16)]

for num in range(1,NumFiles+1):
	fIn[num]  = ROOT.TFile(inputFile[num]) # open ROOT file
	data[num] = fIn[num].Get("data") # get the data tree
time = fIn[num].Get("time") # get the time vector

#run = HVPoint

# Loop over all the events for all channels
#for i in range(0, data[7].GetEntries()+1):
eff = 0
foundClusterSz = 0

# Loop over all the Data Files
for run in range(1,NumFiles+1):


   for i in range(first, last+1):

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
	for n in range(0,15):
		mean[n] = np.mean(pulse[n][:100])
		stdv[n] = np.std(pulse[n][:100])*10.0

#	for j in strips:
	for n in range(0,15):
		low[n]  = 0
		high[n] = 0
		if(debug>2): print "\n-->" + str(n),
#		for j in range(0,600):
		for j in range(100,201):
			if (pulse[n][j]-mean[n]>stdv[n]):
				if(debug>2): print "\t",j,pulse[n][j]-mean[n], low[n]
				if (pulse[n][j]-mean[n]>low[n]):
					low[n] = pulse[n][j]-mean[n]
				else:
					high[n] = low[n]
					if(debug>2): print high[n],
					break
			if (pulse[n][j]-mean[n]>stdv[n] and j==200):
				high[n] = low[n]
				if(debug>2): print high[n],

#		if (j>150 and j<200):
#			if (pulse[n][j]-mean[n] > -1.0*stdv[n]): break
		if(debug>2):
			if (j==599): print "0",
	if(debug>2): print ""

#	#Check amplituds to estimate cluster size
#	for n in range(0,15):
#		if (high[n]>stdv[n]):
#			pass
#		else:
#			if (high[n]!=0): "**** ERROR FOUND ****"

	#Print again amplituds to estimate cluster size
	if(debug>0): print "\n" + str(i) + ")  --> ",
	if(debug>0):
		for n in range(0,15):
			if(debug==2): print " " + str(high[n]) +"("+str(stdv[n])+")",
			if(debug>0 and debug!=2): print " " + str(high[n]),
		print ""

	#Cluster Size Analysis
	consecutive = 0
	clustersize = 0
	for n in range(0,15):
		if (high[n]>0):
			consecutive = 1
			clustersize = clustersize + 1
		else:
			consecutive = 0
			if (clustersize>0):
				if(debug>0): print "\t\tCluster Size = " + str(clustersize)
				if (foundClusterSz==0):
					foundClusterSz = 1
					ClusterSize = [clustersize]
				else:
					ClusterSize.extend([clustersize])
			clustersize = 0
	# If the last strip is over the threshold (10*RMS) print cluster size
	if (clustersize>0): 
		if(debug>0): print "\t\tCluster Size = " + str(clustersize)
		ClusterSize.extend([clustersize])
#	print " Next halt"

   meanClusterSz = np.mean(ClusterSize)
   stdvClusterSz = np.std(ClusterSize)

   if(debug>0): print ""
   print "HV"+str(run)+" "+str(meanClusterSz)+" "+str(stdvClusterSz/sqrt(last-first))
   #/sqrt(last-first)


for num in range(1,NumFiles+1):
	fIn[num].Close()

#inputFile[1]  = "HVSCAN/ecogasboth2/run1/run1.dqm.root"
#inputFile[2]  = "HVSCAN/ecogasboth2/run2/run2.dqm.root"
#inputFile[3]  = "HVSCAN/ecogasboth2/run3/run3.dqm.root"
#inputFile[4]  = "HVSCAN/ecogasboth2/run4/run4.dqm.root"
#inputFile[5]  = "HVSCAN/ecogasboth2/run5/run5.dqm.root"
#inputFile[6]  = "HVSCAN/ecogasboth2/run6/run6.dqm.root"
