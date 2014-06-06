#! /usr/bin/python2.7
import ConfigParser
import random
import string
from faker import Faker
import sqlite3 as lite
import rstr
import io
import sys
import fileinput
import getopt
import os

#cur = con.cursor()
#def sample_wr(values,nn):    
#	return([random.choice(values) for i in xrange(nn)]) 

#def simxegers(simxeger,nn):
#	return([rstr.xeger(simxeger) for i in xrange(nn)])

def makeunique(func, funarg, nn):
	result = []
	while len(result) < nn:
		result.extend(func(funarg,nn))
		result = list(set(result))
	return(result[:nn])

def readDDL(sqlfiles,con):
	#Below is how you do type checking
	if not isinstance(con,lite.Connection): 
		raise ValueError, "The con argument should be a sqlite3.Connection"
	ii = len(sqlfiles)
	if not ii > 0:
		raise TypeError, "The sqlfiles argument must be a list of file names"
	if ii >0 and con is not None: # The length of 
			cur = con.cursor()
			for ii in sqlfiles:
				inputfile = open(ii,'r').read()
				cur.executescript(inputfile) 
#			return 0;
				#for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table'"):
					#print row
#	else:
		#print "Error; Please input .sql files"
#		return 1;

#def printtables(con):
#	cur = con.cursor()
#	for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table'"):
#			print row
#	else:
#		print "Error; Please input .sql files"

def simDB(con):
	if not isinstance(con,lite.Connection): 
		raise ValueError, "The con argument should be a sqlite3.Connection"
	con.row_factory = lite.Row
	cur=con.cursor()
	cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
	done = [] # list of tables that have been created
	for row in cur.fetchall():
		simTable(row[0],con,done,10)


def simTable(tableName,con,done,nn):
	if not isinstance(con,lite.Connection): 
		raise ValueError, "The con argument should be a sqlite3.Connection"
	if tableName in done: 
		'''If tableName is one of the ones in the done 
		list, don't redo it. Just return.'''
		return
	cur = con.cursor()
	if len(cur.execute("SELECT * FROM sqlite_master WHERE type='table' and name='"+tableName+"'").fetchall()) == 0:
		raise NameError(tableName+' dosen\'t exist')
	print '\n'+tableName
	tabletemp = {}
	'''Note about the table_info command:
	the following are the field values returned...
	cid|name|type|notnull|dflt_value|pk
	'''
	for row in cur.execute("PRAGMA table_info("+tableName+")"):
		'''We iterate over all columns in this table
		First, find out the data type'''
		if row[2] == '': ctype = 'varchar'
		else: ctype = row[2]
		'''Now, set simfun to the appropriate 
		function'''
		simfun = {'int': lambda ignore,nn: [random.randint(0,99999) for ii in xrange(nn)],
			  'varchar': lambda ignore,nn: [rstr.postalsafe(10) for ii in xrange(nn)]}[ctype]
		'''Then, find out if it needs to be unique'''
		if row[5] == 1: tabletemp[row[1]] = makeunique(simfun,'',nn)
		else: tabletemp[row[1]] = simfun('',nn)
		print row
	print tabletemp
	'''If we got this far successfully, add this table to
	the done list so it doesn't get done again.'''
	done.append(tableName) 
		
#def simCol(simtype, nn, unique=False, values = [], simxeger = '', fracnull = 0):
#	if len(simxeger) > 0:
#		if unique:
#			result = makeunique(simxegers, simxeger, nn)
#		else:
#			result = simxegers(simxeger, nn)
#	elif len(values) > 0:
#		if unique:
#			result = random.sample(values, nn)
#		else:	
#			result = sample_wr(values, nn)
#	else:           
#		if unique:
#			result simfun = {'NUMBER': lambda ignore,nn: [random.randint(0,99999) for ii in xrange(nn)],'VARCHAR2': lambda ignore,nn: [rstr.postalsafe(10) for ii in xrange(nn)]}[simtype]= makeunique(simfun, 'ComeWorkAtCIRD', nn)
#		else:
#			result = simfun('ItsAwesomeHere',nn)
#	return(result)
		
		
		
if __name__ == "__main__":
	con = lite.connect(":memory:")
	con.text_factory = str
	readDDL(['test.sql'],con)
	done = []
	import pdb; pdb.set_trace() # invoke debugger
	simDB(con)
	#printtables(readDDL)
	#print globals() 			


 



#def writeDB(sqlitedb, filename, filetype):
#	sqlitedb
#	filename
#	filetype
	
