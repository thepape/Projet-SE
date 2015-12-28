#!/usr/bin/python

# Classe representant une machine
#
# CHABOISSIER Maxime
# MARTEAUX Anais
# PAPELIER Romain
# ROLLINGER Jerome
#
# Projet SE 2015 - Simulation d'usinage en temps reel

from threading import Thread
from threading import Lock
import threading
import time
import os
import signal

class Machine(Thread):

	def __init__(self, id_m, types_s, qM, qM2, qR, tpsUa, tpsUb, tpsUc, R, do):
		threading.Thread.__init__(self)
		self.types_supportes = types_s
		#file de la machine
		self.queueM = qM
		#file de l'autre machine
		self.queueM2 = qM2
		#file du robot
		self.queueR = qR
		self.Terminated = False
		self.genTerminee = False

		# on demande les temps d'usinage pour les 3 types, 
		# malgre que la machine n'en prendra en compte que 2,
		# cela permet de n'ecrire qu'une seule classe pour les 2 machines
		self.tempsUsinageA = tpsUa
		self.tempsUsinageB = tpsUb
		self.tempsUsinageC = tpsUc

		self.id = id_m
		self.robot = R
		self.historique = []
		self.dock_only = do

	def stop(self):
		self.Terminated = True

	#indique a la machine que la generation de pieces est terminee.
	#permet de ne pas bloquer la machine lorsque la file est vide et que le generateur a fini.
	def generationTerminee(self):
		self.genTerminee = True

	def getHisto(self):
		return self.historique

	def run(self):
		nb_p_u = 0

		while not self.Terminated:
			
			if self.queueM.empty():
				
				if self.genTerminee:
					self.Terminated = True
					break

				continue

			#bloque si la file est vide et que le generateur n'a pas fini
			p = self.queueM.get()
			

			#verification du type de piece
			if p.type_piece in self.types_supportes:

				#usinage
				tempsUsinage = 1

				if p.type_piece == 'A':
					tempsUsinage = self.tempsUsinageA
				elif p.type_piece == 'B':
					tempsUsinage = self.tempsUsinageB
				else:
					tempsUsinage = self.tempsUsinageC

				p.usiner(tempsUsinage)
				nb_p_u+=1
				self.historique.append(p.type_piece)

				if not self.dock_only:
					print "M{}: Piece {} usinee".format(self.id, p.type_piece)
				
				self.queueR.put(p)

			else:
				#envoi a l'autre Machine
				if not self.dock_only:
					print "M{}: Piece {} envoyee a l'autre machine".format(self.id, p.type_piece)
				
				self.queueM2.put(p)

			#indique qu'un objet de la file a ete usine
			self.queueM.task_done()

		#indique au robot que la machine a fini
		self.robot.machineTerminee()

		if not self.dock_only:
			print "M{} termine. NBPU : {}\n".format(self.id, nb_p_u)
		return
