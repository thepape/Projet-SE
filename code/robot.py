#!/usr/bin/python

from threading import Thread
from threading import Lock
import threading
import time
import os
import signal


class robot(Thread):

	def __init__(self, qR, qA, qB, qC):
		threading.Thread.__init__(self)
		self.queueR = qR
		self.queueA = qA
		self.queueB = qB
		self.queueC = qC
		self.Terminated = False
		self.genTerminee = False
		

	def stop(self):
		self.Terminated = True

	def generationTerminee(self):
		self.genTerminee = True

	def run(self):
		nb_p_u = 0

		while not self.Terminated:
			
			if self.queueR.empty():
				
				if self.genTerminee:
					self.Terminated = True
					break

				continue

			p = self.queueR.get()
			

			#verification du type de piece A
			if p.type_piece == "A":

				#usinage
				p.ranger(self)
				nb_p_u+=1

				print "M{}: Piece {} rangee".format(self.id, p.type_piece)
				self.queueA.put(p)
				
			if p.type_piece == "B":

				#usinage
				p.ranger(self)
				nb_p_u+=1

				print "M{}: Piece {} rangee".format(self.id, p.type_piece)
				self.queueB.put(p)
				
			if p.type_piece == "C":

				#usinage
				p.ranger(self)
				nb_p_u+=1

				print "M{}: Piece {} rangee".format(self.id, p.type_piece)
				self.queueA.put(p)

			#self.queueM.task_done() ??

		print "robot fin. NBPU : {}\n".format( nb_p_u)
		return