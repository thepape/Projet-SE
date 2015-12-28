#! /usr/bin/python 
# -*- coding: utf8 -*- 

# Classe representant un generateur de pieces
#
# CHABOISSIER Maxime
# MARTEAUX Anais
# PAPELIER Romain
# ROLLINGER Jerome
#
# Projet SE 2015 - Simulation d'usinage en temps reel

import os
import sys
import random
#import sysv_ipc
import threading 
import time
from Piece import Piece
import signal

	
		
class GenerateurObjet(threading.Thread):

	#constructeur
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
		
	#permet d'indiquer au generateur de s'arreter
	def stop(self): 
		self.Terminated = True  

	#retourne l'historique de generation
	def getHisto(self):
		return self.historique
    		
    #methode RUN du thread
	def run(self):
		type = ["A", "B", "C"]
		
		queueListe = [self.queue1, self.queue2]
		j = 0

		while not self.Terminated:
			r = random.randint(0,2)
			p = Piece(type[r])
			if j%2 == 0 :
				
				queue = self.queue1
				
				machine = 1
			else :
				
				queue = self.queue2
				
				machine = 2
			j += 1
			

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

		#indique aux machines que la generation est terminee
		self.machine1.generationTerminee()
		self.machine2.generationTerminee()
		
		#print "gen terminee"
		return

