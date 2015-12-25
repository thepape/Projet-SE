#!/usr/bin/python

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
		self.queueM = qM
		self.queueM2 = qM2
		self.queueR = qR
		self.Terminated = False
		self.genTerminee = False
		self.tempsUsinageA = tpsUa
		self.tempsUsinageB = tpsUb
		self.tempsUsinageC = tpsUc
		self.id = id_m
		self.robot = R
		self.historique = []
		self.dock_only = do

	def stop(self):
		self.Terminated = True

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

			self.queueM.task_done()

		self.robot.machineTerminee()

		if not self.dock_only:
			print "M{} termine. NBPU : {}\n".format(self.id, nb_p_u)
		return
