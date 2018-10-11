#! /usr/bin/python3
# -*- coding: utf-8 -*-
from numpy import pi,arcsin,cos,log10,exp,sqrt,zeros,array

"""
	This module give some usefull classes that will contain all satellites communication parameters.
	The power, elevation & datarate are not represented here.
	The module provide the classes:
		-Satellite
		-GroundStation
		-Modulation
		-PropagationChannel
	At the end, a test allow to visualise all parameters stored in each classes.
"""

#Constants
LIGHT_SPEED = 2.99792458e8		#m.s^-1
EARTH_RADUIS = 6371				#km
BOLTZMAN_CONST = 1.38099e-23	#j.k^-1

def real2dB(real): return 10*log10(real)
def dB2real(db): return pow(10,db/10)

class Satellite:
	"""
	The Satellite class handle statics parameters:
		-altitude		(in km)
		-onboard loss	(in dB)
	And elevation functions : f(theta (in °))
		-mispointing 	(in ° )
		-gain				(in dB)
		-axial ratio	(in dB)
	Example :
		>>>sat=Satellite(420,.5,lambda x:abs(90-x),lambda x:6.5,lambda x:3)
		>>>sat.gain(45)
		6.5
		>>>sat.mispointing(25)
		65
	"""
	def __init__(self,altitude,onboard_loss,
					mispointing,gain,axial_ratio):
		"""Init the Satellite class cf Satellite docstrings"""
		self.altitude=altitude
		self.onboard_loss=onboard_loss
		self.mispointing=mispointing
		self.gain=gain
		self.axial_ratio=axial_ratio

class GroundStation:	
	"""
	The GroundStation class handle statics parameters:
		-latitude							(in °N)
		-altitude							(in km)
		-antenna_diameter					(in m)
		-polarisation_ellipse_angle	(in °)
		-min_elevation						(in °)
		-mispointing						(in °)
		-antenna_efficiency
		-axial_ratio						(in dB)
	The GroundStation also store components temperature (in K) and Gain (in dB)
	The Receiver process after the antenna and cable is :
		-LNA
		-mixer
		-IFA
	At the init, the object call computeReceiverGain and computeReceiverTemperature
	to calculate equivalent gain_receiver gain and temp_receiver
	"""
	def __init__(self,latitude,altitude,antenna_diameter,
					polarisation_ellipse_angle,min_elevation,
					mispointing,antenna_efficiency,
					temp_LNA,temp_mixer,temp_cable,temp_IFA,
					gain_LNA,gain_mixer,gain_cable):
		"""Init the GroundStation class cf GroundStation docstrings"""
		self.latitude=latitude
		self.altitude=altitude
		self.antenna_diameter=antenna_diameter
		self.polarisation_ellipse_angle=polarisation_ellipse_angle
		self.min_elevation=min_elevation
		self.mispointing=mispointing
		self.antenna_efficiency=antenna_efficiency
		self.axial_ratio=1
		self.temp_cable=temp_cable
		self.gain_cable=gain_cable
		#Receiver
		self.temp_LNA=temp_LNA
		self.gain_LNA=gain_LNA
		self.temp_mixer=temp_mixer
		self.gain_mixer=gain_mixer
		self.temp_IFA=temp_IFA
		self.gain_IFA=0
	
		self.gain_receiver=self.computeReceiverGain()
		self.temp_receiver=self.computeReceiverTemperature()

	def computeReceiverGain(self):
		"""Compute equivalente receiver gain"""
		return self.gain_LNA+self.gain_mixer+self.gain_IFA

	def computeReceiverTemperature(self):
		"""Compute equivalente receiver temperature"""
		lin_gain_LNA=dB2real(self.gain_LNA)
		lin_gain_mixer=dB2real(self.gain_mixer)
		return self.temp_LNA + self.temp_mixer/lin_gain_LNA + self.temp_IFA/(lin_gain_LNA*lin_gain_mixer)

class Modulation:
	"""
	The Modulation class handle statics parameters:
		-frequence							(in GHz)
		-bits_per_symbol					(in bit/sym)
		-Eb_N0								(in dB)
		-roll_off_factor
		-correcting_code_efficiency
		-min_margin							(in dB)
		-disponibility						(in %)
	QPSK,PSK8 and PSK16 can be use at the init to determine bits_per_symbol

	the method getBitRate convert a data rate in bit rate
	"""
	QPSK = "QPSK"
	PSK8 = "8PSK"
	PSK16="16PSK"

	def __init__(self,frequence,type_mod,Eb_N0,roll_off_factor,
				correcting_code_efficiency,min_margin,disponibility):
		"""Init the Modulation class cf Modulation docstrings"""
		self.frequence=frequence
		self.bits_per_symbol=self.getBitsPerSymbolsWithModulationType(type_mod)
		self.Eb_N0=Eb_N0
		self.roll_off_factor=roll_off_factor
		self.correcting_code_efficiency=correcting_code_efficiency
		self.min_margin=min_margin
		self.disponibility=disponibility

	def getBitsPerSymbolsWithModulationType(self,mod):
		"""return the bits_per_symbol for the Modulation constants"""
		if mod==self.QPSK :return 2
		if mod==self.PSK8 :return 3
		if mod==self.PSK16:return 4
		return 1

	def getBitRate(self,data_rate):
		"""return BitRate from the DataRate, same Unit in and out""" 
		return data_rate/self.correcting_code_efficiency

class PropagationChannel:
	"""
	The PropagationChannel class handle statics parameters:
		-r0_01_rainfall_rate	(mm/h)
		-athmospherical_loss	(in dB)
		-temp_sky				(in K)
		-temp_ground			(in K)
		-temp_weather			(in K)
		-input_antenna_noise	(in K)
	input_antenna_noise is compute at the init with computeInputAntennaNoise method

	"""
	def __init__(self,r0_01_rainfall_rate,athmospherical_loss,
			temp_sky,temp_ground,temp_weather):
		"""Init the PropagationChannel class cf PropagationChannel docstrings"""
		self.r0_01_rainfall_rate=r0_01_rainfall_rate
		self.athmospherical_loss=athmospherical_loss
		self.temp_sky=temp_sky
		self.temp_ground=temp_ground
		self.temp_weather=temp_weather

		self.input_antenna_noise=self.computeInputAntennaNoise()

	def computeInputAntennaNoise(self):
		"""Compute directly antenna noise according to others parameters"""
		real_athmospherical_loss = dB2real(self.athmospherical_loss)
		return self.temp_sky*real_athmospherical_loss + \
					self.temp_weather*(1-1/real_athmospherical_loss) + \
					self.temp_ground


#Validation Tests
if __name__ == "__main__":
	#Interpolation tool
	from scipy.interpolate import interp1d

	#Satellite Gain,mispointing & Axial Ratio
	thetas = array([5,10,20,30,40,50,60,70,80,90])
	gain = array([-7.5,-7.2,-5.7,-3.2,-2.3,-1.1,0.8,3.3,6.1,7.4])
	mispointing = array([85,68,62,54,46,37,28,19,9,0])
	axial_ratio = array([16.5,16.5,18.8,20,14.7,7.2,2.5,5.8,5.5,4.5])
	
	gain = interp1d( thetas, gain )
	mispointing = interp1d( thetas, mispointing )
	axial_ratio = interp1d( thetas, axial_ratio )

	print("\tSatellite Test")
	gomX=Satellite(420,0.5,mispointing,gain,axial_ratio)
	var_gomX=vars(gomX)
	for i in var_gomX : print(i+" \t= "+str(var_gomX[i]))
	
	print("\n\tGround Station Test")
	kurou_station=GroundStation(5.1,300,11.125,45,5,0.1,0.65,
		150,850,290,400,50,-10,-0.5)
	var_kurou=vars(kurou_station)
	for i in var_kurou : print(i+" \t= "+str(var_kurou[i]))

	print("\n\tModulation Test")
	gom_modu=Modulation(8.2,Modulation.QPSK,9.59,0.25,0.5,3,.99)
	var_modu=vars(gom_modu)
	for i in var_modu : print(i+" \t= "+str(var_modu[i]))

	print("\n\tPropagation Test")
	propa=PropagationChannel(85,0.2,20,45,275)
	var_propa=vars(propa)
	for i in var_propa : print(i+" \t= "+str(var_propa[i]))

	print("\n\tdB conversion Test")
	test_dB=152
	print("{0} = {1:2.2f}dB = {2:3.2f}".format(test_dB,real2dB(test_dB),dB2real(real2dB(test_dB)) ) )
	


