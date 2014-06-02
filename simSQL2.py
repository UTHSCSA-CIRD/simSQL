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

con = lite.connect(":memory:")
#cur = con.cursor()
con.text_factory = str
#def sample_wr(values,nn):    
#	return([random.choice(values) for i in xrange(nn)]) 

#def simxegers(simxeger,nn):
#	return([rstr.xeger(simxeger) for i in xrange(nn)])

#def makeunique(func, funarg, nn):
#	result = []
#	while len(result) < nn:
#		result.extend(func(funarg,nn))
#		result = list(set(result))
#   return(result[:nn])

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



def readDDL(sqlfiles,con):
	#import pdb; pdb.set_trace()
	i = len(sqlfiles)
	if i is not None and con is not None:
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
	cur=con.cursor()
	con.row_factory = lite.Row
	cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
	for row in cur.fetchall():
		simTable(con,row[0])


def simTable(con, tableName):
	#tableName = ''
	if not os.path.exists(tableName):
		raise NameError(tableName+'dosen\'t exists')
	cur = con.cursor()
	for row in cur.execute("PRAGMA table_info("+tableName+")"):
		print row
		
		
		
		
if __name__ == "__main__":
	#readDDL([],con)
	readDDL(['test.sql','crc_create_datamart_oracle.sql'],con!=None)
	#printtables(readDDL)
	simTable(['test.sql'],test)
	#print globals() 			


 



#def writeDB(sqlitedb, filename, filetype):
#	sqlitedb
#	filename
#	filetype
	