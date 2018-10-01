#! /usr/bin/python3

#TODO make all comments (why class and units of each parameters)

#Constants
LIGHT_SPEED = 2.99792458e8		#m.s^-1
EARTH_RADUIS = 6371				#km
BOLTZMAN_CONST = 1.38099e-23	#j.k^-1

class Satellite:
	"""Def"""
	def __init__(self,altitude,onboard_loss,
					mispointing,gain,axial_ratio):
		"""init"""
		self.altitude=altitude
		self.onboard_loss=onboard_loss
		self.mispointing=mispointing
		self.gain=gain
		self.axial_ratio=axial_ratio

class GroundStation:
#TODO create a NoisedComponant that handle Temp & gain for a componant and store a list
	"""Def"""
	def __init__(self,Latitude,altitude,antenna_diameter,
					polarisation_ellipse_angle,min_elevation,
					mispointing,antenna_efficiency,
					temp_LNA,temp_mixer,temp_cable,temp_IFA,
					gain_LNA,gain_mixer,gain_cable):
		"""init"""
		self.Latitude=Latitude
		self.altitude=altitude
		self.antenna_diameter=antenna_diameter
		self.polarisation_ellipse_angle=polarisation_ellipse_angle
		self.min_elevation=min_elevation
		self.mispointing=mispointing
		self.antenna_efficiency=antenna_efficiency
		self.temp_LNA=temp_LNA
		self.gain_LNA=gain_LNA
		self.temp_mixer=temp_mixer
		self.gain_mixer=gain_mixer
		self.temp_cable=temp_cable
		self.gain_cable=gain_cable
		self.temp_IFA=temp_IFA

#TODO create QPSK,8PSK,16PSK patern
class Modulation:

	"""Def"""
	def __init__(self,frequence,bits_symbol,Eb_N0,roll_off_factor,
				correcting_code_efficiency,min_margin,disponibility):
		"""init"""
		self.frequence=frequence
		self.bits_symbol=bits_symbol
		self.Eb_N0=Eb_N0
		self.roll_off_factor=roll_off_factor
		self.correcting_code_efficiency=correcting_code_efficiency
		self.min_margin=min_margin
		self.disponibility=disponibility

#TODO optimize GroundStation & PropagationChanel classes
#(séparate antenna temp noise & rain)
class PropagationChanel:
	"""Def"""
	def __init__(self,r0_01_precipitation_intensity,athmospherical_loss,
			temp_sky,temp_ground,temp_weather):
		"""init"""
		self.r0_01_precipitation_intensity=r0_01_precipitation_intensity
		self.athmospherical_loss=athmospherical_loss
		self.temp_sky=temp_sky
		self.temp_ground=temp_ground
		self.temp_weather=temp_weather

	

#Validation Tests






