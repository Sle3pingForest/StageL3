#!/usr/bin/python
# coding: utf-8

import sys
import time
import mysql.connector

#...!....1....!....2....!....3....!....4....!....5....!....6....!....7....!....8
################################################################################

__author__ = 'André Giang <andre.giang8@etu.univ-lorraine.fr>'
__date__, __version__ = '06/06/2018', '1.0'
__description__ = '''
	Connect to database.
'''
__verbose__ = False

################################################################################

def connection():
	config = {
	  'user': 'root',
	  'password': 'azerty',
	  'host': '127.0.0.1',
	  'database': 'Corrector',
	}

	cnx = mysql.connector.connect(**config)

	return cnx
