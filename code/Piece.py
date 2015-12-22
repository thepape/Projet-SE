#!/usr/bin/python

import time

#classe d'une piece a usiner
class Piece:

	type_piece = ''
	est_usinee = False

	def __init__(self,type_p):
		self.type_piece = type_p

	def usiner(temps):
		time.sleep(temps)