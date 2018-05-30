#!/usr/bin/python
# coding: utf-8

import sys
import time
import mysql.connector

def connection():
	config = {
	  'user': 'root',
	  'password': 'azerty',
	  'host': '127.0.0.1',
	  'database': 'Test',
	}

	cnx = mysql.connector.connect(**config)

	return cnx
