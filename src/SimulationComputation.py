#! /usr/bin/python3
# -*- coding: utf-8 -*-
if __name__=="__main__":
	from SimulationObjects import *
	from RainAttenuation import *
else:
	from src.SimulationObjects import *
	from src.RainAttenuation import *

"""
	This module give a class CommunicationSimulation that will contain SimulationObjects.
	This class is design to compute most of the satellite communication formula.

	After create a CommunicationSimulation, you can use the computeMargin that
	return the margin (in dB) of the simulated communication.
	You can provide to this function an array of data (see computeMargin docstrings)
"""

class CommunicationSimulation:
	"""
	The CommunicationSimulation class handle SimulationObjects:
		-satellite
		-ground_station
		-modulation
		-propa_channel
	And will create a RainSpecificAttenuation object at each initialisation

	The class has many methods (see each docstrings):
		-computeBandwidth
		-computePIRE
		-computeDistance
		-computeFreeSpaceLoss
		-computePolaraisationLoss
		-computeFinalReceiverGain
		-computeFinalReceiverTemperature
		-computeFinalReceiverFigureOfMerit
		-computeAllRainAttenuation
		-computeInputReceiverPower
		-computeFinalNoise
		-computeC_N0
		-computeEb_N0
		-computeSpectralEfficiency
		-computeMargin
	"""
	def __init__(self,satellite,ground_station,modulation,propa_channel):
		"""Init the CommunicationSimulation class cf CommunicationSimulation docstrings"""
		self.satellite=satellite
		self.ground_station=ground_station
		self.modulation=modulation
		self.propa_channel=propa_channel
		#Create RainAttenuation class
		self.rain_attenuation=RainSpecificAttenuation(self.propa_channel.r0_01_rainfall_rate,self.modulation.frequence,
					self.satellite.altitude,self.ground_station.altitude,self.ground_station.latitude)

	def computeBandwidth(self,data_rate):
		"""
		:param data_rate: wanted DataRate(in Hz)
		:return: Bandwidth 					(in Hz)
		"""
		t_s=self.modulation.bits_per_symbol/self.modulation.getBitRate(data_rate)
		return (1+self.modulation.roll_off_factor)/t_s

	def computePIRE(self,input_power,theta):
		"""
		:param input_power:			(in W)
		:param theta: Elevation		(in °)
		:return: PIRE 					(in dB)
		"""
		return real2dB(input_power)+self.satellite.gain(theta)

	def computeDistance(self,theta):
		"""
		:param theta: Elevation					(in °)
		:return: Ground-Satellite distance	(in m)
		"""
		#compute Differential latitude
		diff_lat = 90 - theta - 180/pi*arcsin( 
			EARTH_RADUIS/(EARTH_RADUIS+self.satellite.altitude)*cos(pi/180*theta) )
		#compute d^2
		d2 = EARTH_RADUIS**2 + (EARTH_RADUIS+self.satellite.altitude)**2 \
					- 2 * EARTH_RADUIS * (EARTH_RADUIS+self.satellite.altitude) * cos( diff_lat/180*pi )

		return sqrt(d2)*1000#m

	def computeFreeSpaceLoss(self,theta):
		"""
		:param theta: Elevation		(in °)
		:return: Free Space Loss	(in dB)
			Use computeDistance method
		"""
		d=self.computeDistance(theta)
		lamb=LIGHT_SPEED/(self.modulation.frequence*1e9)#GHz

		return 2 * real2dB( lamb/(4*pi*d) )
		
	def computePolaraisationLoss(self,theta):
		"""
		:param theta: Elevation			(in °)
		:return: Polaraisation Loss	(in dB)
		"""
		ar_tx=self.satellite.axial_ratio(theta)
		ar_rx=self.ground_station.axial_ratio
		ellipse_angle=self.ground_station.polarisation_ellipse_angle

		polar_loss = 4*ar_tx*ar_rx + (ar_tx**2-1)*(ar_rx**2-1)*cos(pi/180*2*ellipse_angle)
		polar_loss/= 2*(ar_tx**2+1)*(ar_rx**2+1)
		polar_loss+= 0.5
		
		return real2dB(polar_loss)


	def computeFinalReceiverGain(self):
		"""
		:return: End Receiver Gain	(in dB)
			Use computeGroundAntennaGain method
		"""
		return self.ground_station.gain_receiver+self.ground_station.gain_cable+ self.computeGroundAntennaGain()

	def computeFinalReceiverTemperature(self):
		"""
		:return: End Receiver Temperature	(in K)
		"""
		lin_cable_gain=dB2real(self.ground_station.gain_cable)
		return lin_cable_gain*self.propa_channel.input_antenna_noise + \
				(1-lin_cable_gain)*self.ground_station.temp_cable + self.ground_station.temp_receiver

	def computeGroundAntennaGain(self,mispointing=True):
		"""
		:param mispointing: use mispointing or not
		:return: Ground Antenna Gain	(in dB)
		"""
		lamb=LIGHT_SPEED/(self.modulation.frequence*1e9)#GHz
		theta3dB=70*lamb/self.ground_station.antenna_diameter
		perfect_gain=real2dB(36000/theta3dB**2)

		if mispointing: perfect_gain-= 12* (self.ground_station.mispointing/theta3dB)**2
		return perfect_gain

	def computeFinalReceiverFigureOfMerit(self):
		"""
		:return: Figure of Merit of the reception
			Use computeFinalReceiverTemperature and computeFinalReceiverGain methods
		"""
		T0=290#K
		fig_of_merit=self.computeFinalReceiverTemperature()/T0
		return fig_of_merit/( 1-1/dB2real(self.computeFinalReceiverGain()) )
	
	def computeAllRainAttenuation(self,thetas):
		"""
			Process rain attenuation for single value or array of Elevation
		:param thetas: Elevation(s)		(in °)
		:return: Rain Attenuation			(in dB)
		"""
		#int
		if isinstance(thetas,int):
			self.rain_attenuation.computeAttenuation(thetas)
			return self.rain_attenuation.a0_01_attenuation
		#array
		rain_attenuation_result=zeros(len(thetas))
		for i in range(len(thetas)):
			self.rain_attenuation.computeAttenuation(thetas[i])
			rain_attenuation_result[i]=self.rain_attenuation.a0_01_attenuation
		return rain_attenuation_result

	def computeInputReceiverPower(self,power,theta):
		"""
		:param power: Input power	(in W)
		:param theta: Elevation		(in °)
		:return: Received Power		(in dBw)
			Use computeAllRainAttenuation, computePIRE, computeFreeSpaceLoss, 
		computePolaraisationLoss and computeFinalReceiverGain methods
		"""
		rain_attenuation_result=self.computeAllRainAttenuation(theta)

		return self.computePIRE(power,theta) 			+ \
     			self.computeFreeSpaceLoss(theta)			+ \
      		self.computePolaraisationLoss(theta) 	- \
      		rain_attenuation_result						+ \
				self.computeFinalReceiverGain()

	def computeFinalNoise(self,data_rate):
		"""
		:param data_rate: Wanted DataRate(in Hz)
		:return: Receiver Noise				(in dBw)
			Use computeFinalReceiverTemperature and computeBandwidth methods
		"""
		return real2dB( self.computeFinalReceiverTemperature() * BOLTZMAN_CONST * self.computeBandwidth(data_rate) )

	def computeC_N0(self,power,theta,data_rate):
		"""
		:param power: Input power			(in W)
		:param theta: Elevation				(in °)
		:param data_rate: Wanted DataRate(in Hz)
		:return: C/N0							(in dB)
			Use computeInputReceiverPower and computeFinalNoise methods
		"""
		return self.computeInputReceiverPower(power,theta)-self.computeFinalNoise(data_rate)

	def computeEb_N0(self,power,theta,data_rate):
		"""
		:param power: Input power			(in W)
		:param theta: Elevation				(in °)
		:param data_rate: Wanted DataRate(in Hz)
		:return: Eb/N0							(in dB)
			Use computeC_N0 method
		"""
		return self.computeC_N0(power,theta,data_rate)- real2dB( self.computeBandwidth(data_rate)/ \
						self.modulation.getBitRate(data_rate) )

	def computeSpectralEfficiency(self,data_rate):
		"""
		:param data_rate: Wanted DataRate(in Hz)
		:return: Spectral Efficiency
			Use computeBandwidth method
		"""
		return data_rate/self.computeBandwidth(data_rate)

	def computeMargin(self,power,theta,data_rate):
		"""
		:param power: Input power									(in W)
		:param theta: Elevation										(in °)
		:param data_rate: Wanted DataRate						(in Hz)
		:return: The Margin between Receive power and noise(in dB)
			Use computeEb_N0 method
		"""
		return self.computeEb_N0(power,theta,data_rate) - self.modulation.Eb_N0

