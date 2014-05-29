import ConfigParser
import random
import string
from faker import Faker
import sqlite3 as lite
import rstr
import io
import sys



nn = random.randrange(0, len(f.read()))

def sample_wr(values,nn):
    values = f.read()
    nn = random.randrange(0, len(f.read()))
    return([random.choice(values) for i in xrange(nn)])

def simxegers(simxeger,nn):
    simxeger =  rstr.xeger(r'[A-Z]\d[A-Z] \d[A-Z]\d')
    
    return([rstr.xeger(simxeger) for i in xrange(nn)])

def makeunique(func, funarg, n):
    func = raw_input (funarg, n)
    funarg = simxegers
    n = 100
    result = []
    while len(result) < n:
		result.extend(func(funarg,n))
	return(result)

def simCol(simtype, nn, unique=False, values = [], simxeger = ‘’, fracnull = 0):
	simtype 
	nn = 100
	unique 
	simxeger
	fracnull
	if len(simxeger) > 0:
		if unique:
                        result = makeunique(simxegers, simxeger, nn)
		else:
                        result = simxegers(simxeger, nn)
	elif len(values) > 0:
		if unique:
			result = random.sample(values, nn)
		else:	
                        result = sample_wr(values, nn)

        else

        simtype = "Error; please defind your paramater"
        print simtype
        simfun = {‘NUMBER’: lambda ignore,nn: [random.randint(0,99999) for ii in xrange(nn)],
‘VARCHAR2’: lambda ignore,nn: [rstr.postalsafe(10) for ii in xrange(nn)]		
}[simtype]
       if unique:
	result = makeunique(simfun, ’ComeWorkAtCIRD’, nn)
       else:
	result = simfun(‘ItsAwesomeHere’,nn)

     return(result)



def readDDL(sqlfiles):
       con = lite.connect('test.db')

       with con:
    
       cur = con.cursor()    
       cur.execute('SELECT SQLITE_VERSION()')
    
       data = cur.fetchone()
       print "SQLite version: %s" % data  
       with con:
    
	sqlfiles = 


def simTable(sqlitedb, tableName):
        
	sqlitedb
	tableName
	
       cur = con.cursor()    
       cur.execute("CREATE TABLE testtable(simtype INT, nn INT, unique FLOAT, values = [], simxeger = ‘’, fracnull = 0)")
       cur.execute("INSERT INTO testtable VALUES(1,,52642)")
       cur.execute("INSERT INTO testtable VALUES(2,'Mercedes',57127)")
       cur.execute("INSERT INTO testtable VALUES(3,'Skoda',9000)")
       cur.execute("INSERT INTO testtable VALUES(4,'Volvo',29000)")
       cur.execute("INSERT INTO testtable VALUES(5,'Bentley',350000)")
       cur.execute("INSERT INTO testtable VALUES(6,'Citroen',21000)")
       cur.execute("INSERT INTO testtable VALUES(7,'Hummer',41400)")
       cur.execute("INSERT INTO testtable VALUES(8,'Volkswagen',21600)")


def simDB(sqlitedb):
        sqlitedb



def writeDB(sqlitedb, filename, filetype):
	sqlitedb
	filename
	filetype
