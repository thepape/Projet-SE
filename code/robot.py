#!/usr/bin/python

# Classe representant le robot de rangement
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


class Robot(Thread):

	def __init__(self, qR, lA, lB, lC, tpsA,tpsB,tpsC,nbp):
		threading.Thread.__init__(self)
		self.queueR = qR
		self.listeA = lA
		self.listeB = lB
		self.listeC = lC
		self.Terminated = False
		self.machinesTerminees = 0
		self.tempsA = tpsA
		self.tempsB = tpsB
		self.tempsC = tpsC
		self.historique = []
		self.nbp = nbp
		

	def stop(self):
		self.Terminated = True

	#indique au robot qu'une machine a fini d'usiner.
	#permet au robot de ne pas bloquer lorsque la file est vide et que les machines ont fini
	def machineTerminee(self):
		self.machinesTerminees+=1

	def getHisto(self):
		return self.historique

	def run(self):
		nb_p_r = 0

		while not self.Terminated:
			
			if self.queueR.empty():
				
				if self.machinesTerminees == 2:
					self.Terminated = True
					break

				continue

			#bloque si la file est vide mais que les machines n'ont pas fini d'usiner
			p = self.queueR.get()
			

			#verification du type de piece A
			if p.type_piece == "A":

				#usinage
				p.ranger(self.tempsA)
				self.listeA.append(p)
				nb_p_r+=1


			if p.type_piece == "B":

				#usinage
				p.ranger(self.tempsB)
				nb_p_r+=1
				self.listeB.append(p)
				
			if p.type_piece == "C":

				#usinage
				p.ranger(self.tempsC)
				nb_p_r+=1
				self.listeC.append(p)

			#self.queueM.task_done() ??
			print "R: Piece {} rangee ({}/{})".format(p.type_piece,nb_p_r,self.nbp)
			self.historique.append(p.type_piece)
		print "robot fin.\nNombre de pieces rangees : {}\n".format( nb_p_r)
		return