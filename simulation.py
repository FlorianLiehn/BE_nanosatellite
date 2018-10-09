#! /usr/bin/python3

from src.SimulationComputation import *

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

if __name__ == "__main__":

	#Satellite Gain,mispointing & Axial Ratio
	thetas = np.array([5,10,20,30,40,50,60,70,80,90])
	gain = np.array([-7.5,-7.2,-5.7,-3.2,-2.3,-1.1,0.8,3.3,6.1,7.4])
	mispointing = np.array([85,68,62,54,46,37,28,19,9,0])
	axial_ratio = np.array([16.5,16.5,18.8,20,14.7,7.2,2.5,5.8,5.5,4.5])
	
	gain = interp1d( thetas, gain )
	mispointing = interp1d( thetas, mispointing )
	axial_ratio = interp1d( thetas, axial_ratio )


	#create Satellite
	gomX=Satellite(420,0.5,mispointing,gain,axial_ratio)
	#create GroundStation
	kurou_station=GroundStation(5.1,0.3,11.125,45,5,0.1,0.65,
		150,850,290,400,50,-10,-0.5)
	#create Modulation
	gom_modu=Modulation(8.2,Modulation.QPSK,9.59,0.25,0.5,3,.99)
	#Create PropagationChannel
	propa=PropagationChannel(85,-0.2,20,45,275)
	#Create the final simulation
	simu=CommunicationSimulation(gomX,kurou_station,gom_modu,propa)

	print("Puissance:",simu.computePIRE(1,90)," dBw")
	print("Distance:",simu.computeDistance(45)/1000,"km")
	print("Perte espace libre:",simu.computeFreeSpaceLoss(30),"dB")
	simu.rain_attenuation.computeAttenuation(30)
	print("Rain attenuation 0.01%:",simu.rain_attenuation.a0_01_attenuation,"dB")
	print("Rain attenuation    1%:",simu.rain_attenuation.a1_attenuation,"dB")
	print("Polarisation loss",simu.computePolaraisationLoss(30),"dB")
	print("Antenna Temp",simu.propa_channel.input_antenna_noise,"K")
	print("Receiver Gain",simu.ground_station.gain_receiver,"dB")
	print("Receiver Temp",simu.ground_station.temp_receiver,"K")
	print("Reception Temp",simu.computeFinalReceiverTemperature(),"K")
	print("Antenna gain Perfect",simu.computeGroundAntennaGain(False),"dB")
	print("Antenna gain Real",simu.computeGroundAntennaGain(),"dB")
	print("Reception Gain",simu.computeFinalReceiverGain(),"dB")
	print("Figure of Merit",simu.computeFinalReceiverFigureOfMerit())
	print("")
	print("Input Power",simu.computeInputReceiverPower(1,30), "dBw")
	print("Bandwidth",simu.computeBandwidth(2e6), "Hz")
	print("Input Noise",simu.computeFinalNoise(2e6), "dB")
	print("C/N0",simu.computeC_N0(1,30,2e6), "dB")
	print("Eb/N0",simu.computeEb_N0(1,30,2e6), "dB")
	print("Spectral Efficiency",simu.computeSpectralEfficiency(2e6))
	print("")
	print("Marge",simu.computeMargin(1,30,2e6),"dB")

	#Second part Exploit different values
	thetas = np.linspace(5,90,100)

	margins=simu.computeMargin(1,thetas,2e6)
	plt.plot(thetas,margins)
	plt.show()

