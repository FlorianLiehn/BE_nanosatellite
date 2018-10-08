#! /usr/bin/python3

if __name__=="__main__":
	from SimulationObjects import *
	from RainAttenuation import *
else:
	from src.SimulationObjects import *
	from src.RainAttenuation import *

#TODO make all comments (why class, units of each parameters & where come from the formula)



                

class CommunicationSimulation:
	"""Def"""
	def __init__(self,satellite,ground_station,modulation,propa_channel):
		"""init"""
		self.satellite=satellite
		self.ground_station=ground_station
		self.modulation=modulation
		self.propa_channel=propa_channel
		#Create RainAttenuation class
		self.rain_attenuation=RainSpecificAttenuation(self.propa_channel.r0_01_rainfall_rate,self.modulation.frequence,
					self.satellite.altitude,self.ground_station.altitude,self.ground_station.latitude)

	def computeBandwidth(self,data_rate):
		t_s=self.modulation.bits_per_symbol/self.modulation.getBitRate(data_rate)
		return (1+self.modulation.roll_off_factor)/t_s

	def computePIRE(self,input_power,theta):
		return real2dB(input_power)+self.satellite.gain(theta)

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
		ar_tx=self.satellite.axial_ratio(theta)
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
		self.rain_attenuation.computeAttenuation(theta)
		return self.computePIRE(power,theta) 			+ \
     			self.computeFreeSpaceLoss(theta)			+ \
      		self.computePolaraisationLoss(theta) 	- \
      		self.rain_attenuation.a0_01_attenuation+ \
				self.computeFinalReceiverGain()

	def computeFinalNoise(self,data_rate):
		return real2dB( self.computeFinalReceiverTemperature() * BOLTZMAN_CONST * self.computeBandwidth(data_rate) )

	def computeC_N0(self,power,theta,data_rate):
		return self.computeInputReceiverPower(power,theta)-self.computeFinalNoise(data_rate)

	def computeEb_N0(self,power,theta,data_rate):
		return self.computeC_N0(power,theta,data_rate)- real2dB( self.computeBandwidth(data_rate)/ \
				self.modulation.getBitRate(data_rate)*self.modulation.bits_per_symbol)

	def computeSpectralEfficiency(self,data_rate):
		return data_rate/self.computeBandwidth(data_rate)

	def computeMargin(self,power,theta,data_rate):
		"""detail"""
		return self.computeEb_N0(power,theta,data_rate) - self.modulation.Eb_N0

