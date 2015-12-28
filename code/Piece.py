#!/usr/bin/python

# Classe representant une piece
#
# CHABOISSIER Maxime
# MARTEAUX Anais
# PAPELIER Romain
# ROLLINGER Jerome
#
# Projet SE 2015 - Simulation d'usinage en temps reel

import time


class Piece:

	type_piece = ''
	est_usinee = False
	estrangee = False

	def __init__(self,type_p):
		self.type_piece = type_p

	def usiner(self,temps):
		time.sleep(temps)
		self.est_usinee = True
		
	def ranger(self, temps):
		time.sleep(temps)
		self.est_rangee = True