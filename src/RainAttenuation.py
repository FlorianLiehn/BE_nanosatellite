#! /usr/bin/python3

if __name__=="__main__":
	from SimulationObjects import *
else:
	from src.SimulationObjects import *
	from src.SimulationComputation import *

	from math import *

#TODO make all comments (why class, units of each parameters & where come from the formula)





class RainSpecificAttenuation :
        kh_coefficient= [[-5.33980,-0.10008,1.13098],[-0.35351,1.26970,0.4540],[-0.23789,0.86036,0.15354],[-0.94158,0.64552,0.16817],-0.18961,0.71147]
        kv_coefficient= [[-3.80595,0.56934,0.81061],[-3.44965,-0.22911,0.51059],[-0.39902,0.73042,0.11899],[0.50167,1.07319,0.27195],-0.16398,0.63297]
        alphah_coefficient= [[-0.14318,1.82442,-0.55187],[0.29591,0.77564,0.19822],[0.32177,0.63773,0.13164],[-5.37610,-0.96230,1.47828],[16.1721,-3.29980,3.43990],0.67849,-1.95537]
        alphav_coefficient= [[-0.07771,2.33840,-0.76284],[0.56727,0.95545,0.54039],[-0.20238,1.14520,0.26809],[-48.2991,0.791669,0.116226],[45.5833,0.791459,0.116479],-0.053739,0.83433]
        tau=45
        theta=30
        

        def formuleCoefficient(self,matrice,f):
                somme = 0
                for i in range(len(matrice)-2):
                        somme+= matrice[i][0]*exp(-((log10(f)-matrice[i][1])/matrice[i][2])**2)
                    
                        print(somme)
                somme+= matrice[-2]*log10(f) + matrice[-1]
                
                return somme
        

        
        def __init__(self,r0_01_rainfall_rate,frequence,theta):

                self.kh = pow(10,self.formuleCoefficient(self.kh_coefficient,frequence))
                self.kv = pow(10,self.formuleCoefficient(self.kv_coefficient,frequence))
                self.alphah = self.formuleCoefficient(self.alphah_coefficient,frequence)
                self.alphav = self.formuleCoefficient(self.alphav_coefficient,frequence)
                self.k = (self.kh + self.kv + (self.kh - self.kv)*cos(self.theta*pi/180)*cos(self.theta*pi/180)*cos(2*self.tau*pi/180))/2
                self.alpha = (self.kh*self.alphah + self.kv*self.alphav + (self.kh*self.alphah - self.kv*self.alphav)*cos(self.theta*pi/180)*cos(self.theta*pi/180)*cos(2*self.tau*pi/180))/2*self.k
                self.rain_specific_attenuation = self.k*pow(r0_01_rainfall_rate,self.alpha)


-5.33980*exp(-((log10(8.2)+0.10008)/1.13098)**2)
