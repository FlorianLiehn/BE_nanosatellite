#! /usr/bin/python3

from src.SimulationComputation import *


if __name__ == "__main__":
	#create Satellite
	gomX=Satellite(420,0.5,54,-3.2,20)
	#create GroundStation
	kurou_station=GroundStation(5.1,300,11.125,45,5,0.1,0.65,
		150,850,290,400,50,-10,-0.5)
	#create Modulation
	gom_modu=Modulation(8.2,2,9.59,0.25,0.5,3,.99)
	#Create PropagationChannel
	propa=PropagationChannel(85,0.2,20,45,275)
	#Create the final simulation
	simu=CommunicationSimulation(gomX,kurou_station,gom_modu,propa)

	print("puissance:",simu.computePIRE(1,90)," dBw")
	print("distance:",simu.computeDistance(45),"km")
