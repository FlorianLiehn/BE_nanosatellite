#! /usr/bin/python3



from math import *
    

#TODO make all comments (why class, units of each parameters & where come from the formula)





class RainSpecificAttenuation :
    kh_coefficient= [[-5.33980,-0.10008,1.13098],[-0.35351,1.26970,0.4540],[-0.23789,0.86036,0.15354],[-0.94158,0.64552,0.16817],-0.18961,0.71147]
    kv_coefficient= [[-3.80595,0.56934,0.81061],[-3.44965,-0.22911,0.51059],[-0.39902,0.73042,0.11899],[0.50167,1.07319,0.27195],-0.16398,0.63297]
    alphah_coefficient= [[-0.14318,1.82442,-0.55187],[0.29591,0.77564,0.19822],[0.32177,0.63773,0.13164],[-5.37610,-0.96230,1.47828],[16.1721,-3.29980,3.43990],0.67849,-1.95537]
    alphav_coefficient= [[-0.07771,2.33840,-0.76284],[0.56727,0.95545,0.54039],[-0.20238,1.14520,0.26809],[-48.2991,0.791669,0.116226],[45.5833,0.791459,0.116479],-0.053739,0.83433]
    tau=45
    Re= 8500 #effective radius of the earth


    def formuleCoefficient(self,matrice,f):
        somme = 0
        for i in range(len(matrice)-2):
            somme+= matrice[i][0]*exp(-((log10(f)-matrice[i][1])/matrice[i][2])**2)

            somme+= matrice[-2]*log10(f) + matrice[-1]

        return somme

    def longueurEffectivePluie(self,frequence):

        if self.theta < 5:
            ls = (2*(self.hr-self.hs))/((sin(self.theta*pi/180)*sin(self.theta*pi/180) + (2*(self.hr-self.hs))/Re)**0.5 + sin(self.theta*pi/180))
        else:
            ls = (self.hr-self.hs)/sin(self.theta*pi/180)

        lg=ls*cos(self.theta*pi/180)

        r0_01=1/(1+0.78*(lg*self.rain_specific_attenuation/frequence)**0.5 - 0.38*(1-exp(-2*lg)))

        z=degrees(atan((self.hr-self.hs)/(lg*r0_01)))

        if z>self.theta:
            lr=lg*r0_01/cos(self.theta*pi/180)
        else:
            lr=(self.hr-self.hs)/sin(self.theta*pi/180)

        if abs(self.phi)<36:
            X=36-abs(self.phi)
        else:
            X=0

        v0_01 = 1/(1+sqrt(sin(self.theta*pi/180))*(31*(1-exp(-self.theta/(1+X)))*(sqrt(lr*self.rain_specific_attenuation)/frequence**2)-0.45))

        le=lr*v0_01
        return(v0_01,le)





    def __init__(self,r0_01_rainfall_rate,frequence,sat_alti,station_alti,latitude):
                
        self.h0=2.720
        self.hr=0 + 0.36      
        self.hs=station_alti  #altitude station sol en km
        self.phi=latitude       #°N
        self.r0_01_rainfall_rate=r0_01_rainfall_rate
        self.frequence=frequence

        self.kh = pow(10,self.formuleCoefficient(self.kh_coefficient,frequence))
        self.kv = pow(10,self.formuleCoefficient(self.kv_coefficient,frequence))
        self.alphah = self.formuleCoefficient(self.alphah_coefficient,frequence)
        self.alphav = self.formuleCoefficient(self.alphav_coefficient,frequence)
        self.theta = self.k = self.alpha = self.rain_specific_attenuation = self.a0_01_attenuation = self.a1_attenuation = 0

    def computeAttenuation(self,theta):

        self.theta=theta
        self.k = (self.kh + self.kv + (self.kh - self.kv)*cos(self.theta*pi/180)*cos(self.theta*pi/180)*cos(2*self.tau*pi/180))/2
        self.alpha = (self.kh*self.alphah + self.kv*self.alphav + (self.kh*self.alphah - self.kv*self.alphav)*cos(self.theta*pi/180)*cos(self.theta*pi/180)*cos(2*self.tau*pi/180))/(2*self.k)
        self.rain_specific_attenuation = self.k*pow(self.r0_01_rainfall_rate,self.alpha)
        self.a0_01_attenuation = self.rain_specific_attenuation*self.longueurEffectivePluie(self.frequence)[1]
        self.a1_attenuation = self.a0_01_attenuation*pow(100,-(0.655 + 0.033*log(1)-0.045*log(self.a0_01_attenuation)))



        
        
