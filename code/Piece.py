#!/usr/bin/python

import time

#classe d'une piece a usiner
class Piece:

	type_piece = ''
	est_usinee = False
	estrangee = False

	def __init__(self,type_p):
		self.type_piece = type_p

	def usiner(self,temps):
		time.sleep(temps)
		self.est_usinee = True
		
	def ranger(self):
		self.est_rangee = True