#! /usr/bin/python3

from math import pi,asin,cos,log10,exp,sqrt
if __name__=="__main__":
	from SimulationObjects import *
else:
	from src.SimulationObjects import *

#TODO make all comments (why class, units of each parameters & where come from the formula)




class CommunicationSimulation:
	"""Def"""
	def __init__(self,satellite,ground_sation,modulation,propa_channel):
		"""init"""
		self.satellite=satellite
		self.ground_sation=ground_sation
		self.modulation=modulation
		self.propa_channel=propa_channel
		#Create & compute EquationComputerClasses
		#TODO create all classes needed

	def power2dB(self,power):return 10*log10(power)
	def dB2power(self,db):return 10*pow(10,db)

	def computePIRE(self,input_power,theta):
		return self.power2dB(input_power)+self.satellite.gain

	def computeDistance(self,theta):
		#compute Differential latitude
		diff_lat = 90 - theta - 180/pi*asin( 
			EARTH_RADUIS/(EARTH_RADUIS+self.satellite.altitude)*cos(pi/180*theta) )
		#compute d^2
		d2 = EARTH_RADUIS**2 + (EARTH_RADUIS+self.satellite.altitude)**2 \
					- 2 * EARTH_RADUIS * (EARTH_RADUIS+self.satellite.altitude) * cos( diff_lat/180*pi )

		return sqrt(d2)
	
	def computeMargin(self,theta,input_power,data_rate):
		"""detail"""
		#TODO compute all dynamics values & return margin
		return 0
