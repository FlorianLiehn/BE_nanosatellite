#! /usr/bin/python3
# -*- coding: utf-8 -*-
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

	demo_elevation=30		#°
	demo_power=1			#W
	demo_data_rate=2e6	#Hz
	print("\tDemo elevation {}° input power {}W DataRate {}MHz".format(
						demo_elevation,demo_power,demo_data_rate/1e6) )
	print("Puissance:",simu.computePIRE(demo_power,demo_elevation)," dBw")
	print("Distance:",simu.computeDistance(demo_elevation)/1000,"km")
	print("Perte espace libre:",simu.computeFreeSpaceLoss(demo_elevation),"dB")
	simu.rain_attenuation.computeAttenuation(demo_elevation)
	#TODO Need the d)e)f) answers
	print("Rain attenuation 0.01%:",simu.rain_attenuation.a0_01_attenuation,"dB")
	print("Rain attenuation    1%:",simu.rain_attenuation.a1_attenuation,"dB")
	print("Polarisation loss",simu.computePolaraisationLoss(demo_elevation),"dB")
	print("Antenna Temp",simu.propa_channel.input_antenna_noise,"K")
	print("Receiver Gain",simu.ground_station.gain_receiver,"dB")
	print("Receiver Temp",simu.ground_station.temp_receiver,"K")
	print("Reception Temp",simu.computeFinalReceiverTemperature(),"K")
	print("Antenna gain Perfect",simu.computeGroundAntennaGain(False),"dB")
	print("Antenna gain Real",simu.computeGroundAntennaGain(),"dB")
	print("Reception Gain",simu.computeFinalReceiverGain(),"dB")
	print("Figure of Merit",simu.computeFinalReceiverFigureOfMerit())
	print("")
	print("Input Power",simu.computeInputReceiverPower(demo_power,demo_elevation), "dBw")
	print("Input Noise",simu.computeFinalNoise(demo_data_rate), "dB")
	print("C/N0",simu.computeC_N0(demo_power,demo_elevation,demo_data_rate), "dB")
	print("Eb/N0",simu.computeEb_N0(demo_power,demo_elevation,demo_data_rate), "dB")
	print("Bandwidth",simu.computeBandwidth(demo_data_rate), "Hz")
	print("Spectral Efficiency",simu.computeSpectralEfficiency(demo_data_rate))
	print("")
	print("Marge",simu.computeMargin(1,30,2e6),"dB")

	try:
		choice=input("Press a key to process full simulation (q to quit): ")
		if "q" in choice.lower():raise Exception("User Exit")
	except:
		exit(0)	
	#Second part Exploit different values
	thetas = np.linspace(5,90,100)
	data_rates = np.linspace(100e6,1000e6,100)
	input_powers = np.linspace(1e-3,1,100)
	#Compute all Tests
	nominal_margins = simu.computeMargin(1,thetas,2e6)
	great_data_rate_margins = simu.computeMargin(1,thetas,4.8e6)
	fixed_elevation_margins_rates = simu.computeMargin(1,20,data_rates)
	fixed_elevation_margins_powers = simu.computeMargin(input_powers,20,4.8e6)
	#Plot results
	plt.figure(1)
	plt.plot(thetas,nominal_margins,label='2MHz')
	plt.plot(thetas,great_data_rate_margins,label='4.8MHz')
	plt.plot(thetas,[simu.modulation.min_margin for i in thetas],"r--")
	plt.legend(loc=4)
	plt.title("Marge en fonction de l'élevation à 1W")
	plt.xlabel("°")
	plt.ylabel("dB")

	plt.figure(2)
	plt.plot(data_rates,fixed_elevation_margins_rates)	
	plt.plot(data_rates,[simu.modulation.min_margin for i in data_rates],"r--")
	plt.title("Marge en fonction du débit à 1W et 20° d'élévation")
	plt.xlabel("Hz")
	plt.ylabel("dB")

	plt.figure(3)
	plt.plot(input_powers,fixed_elevation_margins_powers)	
	plt.plot(input_powers,[simu.modulation.min_margin for i in input_powers],"r--")
	plt.title("Marge en fonction de la puissance d'émission à 20° d'élévation et 4.8MHz")
	plt.xlabel("W")
	plt.ylabel("dB")

	plt.show()

