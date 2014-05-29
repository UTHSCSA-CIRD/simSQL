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


con = lite.connect(":memory:")

# def sample_wr(values,nn):
    
    # return([random.choice(values) for i in xrange(nn)]) 

# def simxegers(simxeger,nn):
    
    # return([rstr.xeger(simxeger) for i in xrange(nn)])

# def makeunique(func, funarg, nn):
    # result = []
    # while len(result) < nn:
	# result.extend(func(funarg,nn))
	# result = list(set(result))
    # return(result[:nn])

# def simCol(simtype, nn, unique=False, values = [], simxeger = '', fracnull = 0):
    # if len(simxeger) > 0:
		# if unique:
                # result = makeunique(simxegers, simxeger, nn)
		# else:
                # result = simxegers(simxeger, nn)
	# elif len(values) > 0:
		# if unique:
			# result = random.sample(values, nn)
		# else:	
                        # result = sample_wr(values, nn)

        # else   
        
       # if unique:
	# result simfun = {'NUMBER': lambda ignore,nn: [random.randint(0,99999) for ii in xrange(nn)],
# 'VARCHAR2': lambda ignore,nn: [rstr.postalsafe(10) for ii in xrange(nn)]		
# }[simtype]= makeunique(simfun, 'ComeWorkAtCIRD', nn)
       # else:
	# result = simfun('ItsAwesomeHere',nn)

     # return(result)



def readDDL(sqlfiles,con):
	#import pdb; pdb.set_trace()
	i = len([sqlfiles])
	if i is not None and con is None:
			con = lite.connect(":memory:")
			cur = con.cursor()
			for ii in sqlfiles:
				inputfile = open(ii,'r').read()
				cur.executescript(inputfile)
				for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table'"):
					print row
	else:
		print "Error"
		

def printtable(		


   	
	
if __name__ == "__main__":
	#readDDL([],con)
	readDDL(['test.sql','crc_create_datamart_oracle.sql'],con)
	#print globals() 
	

	

#def simTable(sqlitedb, tableName):
        
#	sqlitedb
#	tableName
	
 #      cur = con.cursor()    
  #     cur.execute("CREATE TABLE testtable(simtype INT, nn INT, unique FLOAT, values = [], simxeger = '', fracnull = 0)")
     


#def simDB(sqlitedb):
 #       sqlitedb



#def writeDB(sqlitedb, filename, filetype):
#	sqlitedb
#	filename
#	filetype
	