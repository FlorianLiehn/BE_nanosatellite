#! /usr/bin/python3

from SimulationObjects import *

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

	def computeMargin(theta,input_power,data_rate):
		"""detail"""
		#TODO compute all dynamics values & return margin
		return 0
