#! /usr/bin/python3

if __name__=="__main__":
	from SimulationObjects import *
else:
	from src.SimulationObjects import *

#TODO make all comments (why class, units of each parameters & where come from the formula)



                

class CommunicationSimulation:
	"""Def"""
	def __init__(self,satellite,ground_station,modulation,propa_channel):
		"""init"""
		self.satellite=satellite
		self.ground_station=ground_station
		self.modulation=modulation
		self.propa_channel=propa_channel
		#Create & compute EquationComputerClasses
		#TODO create all classes needed


	def computePIRE(self,input_power,theta):
		return real2dB(input_power)+self.satellite.gain

	def computeDistance(self,theta):
		#compute Differential latitude
		diff_lat = 90 - theta - 180/pi*asin( 
			EARTH_RADUIS/(EARTH_RADUIS+self.satellite.altitude)*cos(pi/180*theta) )
		#compute d^2
		d2 = EARTH_RADUIS**2 + (EARTH_RADUIS+self.satellite.altitude)**2 \
					- 2 * EARTH_RADUIS * (EARTH_RADUIS+self.satellite.altitude) * cos( diff_lat/180*pi )

		return sqrt(d2)*1000#m

	def computeFreeSpaceLoss(self,theta):
		d=self.computeDistance(theta)
		lamb=LIGHT_SPEED/(self.modulation.frequence*1e9)#GHz

		return 2 * real2dB( lamb/(4*pi*d) )
		
	def computePolaraisationLoss(self,theta):
		ar_tx=self.satellite.axial_ratio
		ar_rx=self.ground_station.axial_ratio
		ellipse_angle=self.ground_station.polarisation_ellipse_angle

		polar_loss = 4*ar_tx*ar_rx + (ar_tx**2-1)*(ar_rx**2-1)*cos(pi/180*2*ellipse_angle)
		polar_loss/= 2*(ar_tx**2+1)*(ar_rx**2+1)
		polar_loss+= 0.5
		
		return real2dB(polar_loss)


	def computeFinalReceiverGain(self):
		return self.ground_station.gain_receiver+self.ground_station.gain_cable+ self.computeGroundAntennaGain()

	def computeFinalReceiverTemperature(self):
		lin_cable_gain=dB2real(self.ground_station.gain_cable)
		return lin_cable_gain*self.propa_channel.input_antenna_noise + \
				(1-lin_cable_gain)*self.ground_station.temp_cable + self.ground_station.temp_receiver

	def computeGroundAntennaGain(self,mispointing=True):
		lamb=LIGHT_SPEED/(self.modulation.frequence*1e9)#GHz
		theta3dB=70*lamb/self.ground_station.antenna_diameter
		perfect_gain=real2dB(36000/theta3dB**2)

		if mispointing: perfect_gain-= 12* (self.ground_station.mispointing/theta3dB)**2
		return perfect_gain

	def computeFinalReceiverFigureOfMerit(self):
		T0=290
		fig_of_merit=self.computeFinalReceiverTemperature()/T0
		return fig_of_merit/( 1-1/dB2real(self.computeFinalReceiverGain()) )
	
	def computeInputReceiverPower(self,power,theta):#TODO use rain attenuation
		return self.computePIRE(power,theta) 			+ \
     			self.computeFreeSpaceLoss(theta)			+ \
      		self.computePolaraisationLoss(theta) 	+ \
				self.computeFinalReceiverGain()			#+ \

	def computeMargin(self,theta,input_power,data_rate):
		"""detail"""
		#TODO compute all dynamics values & return margin
		return 0

