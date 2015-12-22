#! /usr/bin/python 
# -*- coding: utf8 -*- 
import os
import sys
import random
import sysv_ipc
import threading 

class Objet	:
	def __init__(self, type):
		self.type = type
		
		
class GenerateurObjet(threading.Thread):

	def __init__(self, q1, q2, nom):
		threading.Thread.__init__(self)
		self.Terminated = False 
		self.queue1 = q1
		self.queue2 = q2
		self.nom = nom
		
	def stop(self): 
		self.Terminated = True  
    		
	def run(self):
		type = ["A", "B", "C"]
		print(self.nom)
		queueListe = [self.queue1, self.queue2]
		j = 0
		while not self.Terminated:
			r = random.randint(0,2)
			o = Objet(type[r])
			if j%2 == 0 :
				queue = sysv_ipc.MessageQueue(self.queue1)
			else :
				queue = sysv_ipc.MessageQueue(self.queue2)
			j += 1
			queue.send(o.type)
			print("J'ai envoye un objet de type ", o.type, " dans la file ",queue)
