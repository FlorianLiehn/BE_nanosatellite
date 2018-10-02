#! /usr/bin/python3

from math import pi,asin,cos,log10,exp,sqrt
if __name__=="__main__":
	from SimulationObjects import *
else:
	from src.SimulationObjects import *

#TODO make all comments (why class, units of each parameters & where come from the formula)


class RainAttenuation :
        kh_coefficient= [[-5.33980,-0.10008,1.13098],[-0.35351,1.26970,0.4540],[-0.23789,0.86036,0.15354],[-0.94158,0.64552,0.16817],-0.18961,0.71147]
        kv_coefficient= [[-3.80595,0.56934,0.81061],[-3.44965,-0.22911,0.51059],[-0.39902,0.73042,0.11899],[0.50167,1.07319,0.27195],-0.16398,0.63297]
        alphah_coefficient= [[-0.14318,1.82442,-0.55187],[0.29591,0.77564,0.19822],[0.32177,0.63773,0.13164],[-5.37610,-0.96230,1.47828],[16.1721,-3.29980,3.43990],0.67849,-1.95537]
        alphav_coefficient= [[-0.07771,2.33840,-0.76284],[0.56727,0.95545,0.54039],[-0.20238,1.14520,0.26809],[-48.2991,0.791669,0.116226],[45.5833,0.791459,0.116479],-0.053739,0.83433]
        tau=45

        def formuleCoefficient(self,matrice,f):
                somme = 0
                for i in range(len(matrice)-2):
                        somme+= matrice[i][0]*math.exp(((-log10(f)-matrice[i][1])/matrice[i][2])**2)
                somme+= matrice[5]*log10(f) + matrice[6]
                return somme
        


        
        def __init__(self,attenuation_specifique_pluie,frequence):

                self.kh = pow(10,formuleCoefficient(kh_coefficient,frequence))
                

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

		return sqrt(d2)*1000#m

	def computeFreeSpaceLoss(self,theta):
		d=self.computeDistance(theta)
		lamb=LIGHT_SPEED/(self.modulation.frequence*1e9)#GHz

		return 2 * self.power2dB( lamb/(4*pi*d) )
		
	
	def computeMargin(self,theta,input_power,data_rate):
		"""detail"""
		#TODO compute all dynamics values & return margin
		return 0

