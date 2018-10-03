#! /usr/bin/python3

from math import pi,asin,cos,log10,exp,sqrt

#TODO make all comments (why class and units of each parameters)

#Constants
LIGHT_SPEED = 2.99792458e8		#m.s^-1
EARTH_RADUIS = 6371				#km
BOLTZMAN_CONST = 1.38099e-23	#j.k^-1

def real2dB(real):return 10*log10(real)
def dB2real(db):return pow(10,db/10)

class Satellite:
#TODO make mispointing, gain & axial ration function of theta 
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

#TODO optimize GroundStation & PropagationChannel classes
#(séparate antenna temp noise & rain)
class PropagationChannel:
	"""Def"""
	def __init__(self,r0_01_precipitation_intensity,athmospherical_loss,
			temp_sky,temp_ground,temp_weather):
		"""init"""
		self.r0_01_precipitation_intensity=r0_01_precipitation_intensity
		self.athmospherical_loss=athmospherical_loss
		self.temp_sky=temp_sky
		self.temp_ground=temp_ground
		self.temp_weather=temp_weather

		self.input_antenna_noise=self.computeInputAntennaNoise()

	def computeInputAntennaNoise(self):
		real_athmospherical_loss = dB2real(self.athmospherical_loss)
		return self.temp_sky*real_athmospherical_loss + \
					self.temp_weather*(1-1/real_athmospherical_loss) + \
					self.temp_ground


#Validation Tests
if __name__ == "__main__":
	print("\tSatellite Test")
	gomX=Satellite(420,0.5,54,-3.2,20)
	var_gomX=vars(gomX)
	for i in var_gomX : print(i+" \t= "+str(var_gomX[i]))
	
	print("\n\tGround Station Test")
	kurou_station=GroundStation(5.1,300,11.125,45,5,0.1,0.65,
		150,850,290,400,50,-10,-0.5)
	var_kurou=vars(kurou_station)
	for i in var_kurou : print(i+" \t= "+str(var_kurou[i]))

	print("\n\tModulation Test")
	gom_modu=Modulation(8.2,2,9.59,0.25,0.5,3,.99)
	var_modu=vars(gom_modu)
	for i in var_modu : print(i+" \t= "+str(var_modu[i]))

	print("\n\tPropagation Test")
	propa=PropagationChannel(85,0.2,20,45,275)
	var_propa=vars(propa)
	for i in var_propa : print(i+" \t= "+str(var_propa[i]))

	print("\n\tdB conversion Test")
	test_dB=152
	print("{0} = {1:2.2f}dB = {2:3.2f}".format(test_dB,real2dB(test_dB),dB2real(real2dB(test_dB)) ) )
	


