#! /usr/bin/python 
# -*- coding: utf8 -*- 
import os
import sys
import random
#import sysv_ipc
import threading 
import time
from Piece import Piece
import signal

class Objet	:
	def __init__(self, type):
		self.type = type
		
		
class GenerateurObjet(threading.Thread):

	def __init__(self, q1, q2, nom, nb_p,tps_gen, M1,M2,do):
		threading.Thread.__init__(self)
		self.Terminated = False 
		self.queue1 = q1
		self.queue2 = q2
		self.nom = nom
		self.nb_pieces = nb_p
		self.machine1 = M1
		self.machine2 = M2
		self.tempsGen = tps_gen
		self.historique = []
		self.dock_only = do
		
	def stop(self): 
		self.Terminated = True  

	def getHisto(self):
		return self.historique
    		
	def run(self):
		type = ["A", "B", "C"]
		
		queueListe = [self.queue1, self.queue2]
		j = 0

		while not self.Terminated:
			r = random.randint(0,2)
			p = Piece(type[r])
			if j%2 == 0 :
				#queue = sysv_ipc.MessageQueue(self.queue1)
				queue = self.queue1
				
				machine = 1
			else :
				#queue = sysv_ipc.MessageQueue(self.queue2)
				queue = self.queue2
				
				machine = 2
			j += 1
			#queue.send(o.type)

			#generation piece
			time.sleep(self.tempsGen)

			queue.put(p)

			if not self.dock_only:
				print "G: Piece non usinee {} envoyee a M{}".format(p.type_piece,machine)
			self.historique.append(p.type_piece)

			if j >= self.nb_pieces:
				self.Terminated = True

		#attend que tous les objets envoyés à M1 et M2 soient usinés
		self.queue1.join()
		self.queue2.join()

		#indique aux machines qu'elles peuvent arreter
		self.machine1.generationTerminee()
		self.machine2.generationTerminee()
		
		#print "gen terminee"
		return

