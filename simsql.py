'''
This program is copyright Bob Chien, Angela Bos, Alfredo Tirado-Ramos, and Alex Bokov, 2014.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along
with this program; if not, you can obtain it from http://www.gnu.org/licenses/lgpl-2.1.html
'''


#### Functional Specification, a.k.a. Requirements, a.k.a. User Story ####
''' You have a large database, and it’s top-secret so you are very limited in 
what you can do with the data. You want the same data types, in the same 
schema, but completely simulated so you can explore it, demo it, test against
it, without getting sued or fired. However, the empty schema is not secret. So,
you dump just the schema into an SQL file and you run this script against it. 
The script parses out the table structures, the primary keys, and the foreign 
keys. Then, it creates an internal representation of this database and fills it with 
random values of the correct type, with foreign key relationships intact. You also
give the script a config file that indicates how many rows there should be in each
table. The config file also specifies the default number of rows, for tables that 
arent assigned an individual size. Perhaps you have prior knowledge about the
data which is not captured by the SQL dump. You can use the config file to assign 
value lists, custom data types, fraction of missing values, and xegers (inverted 
regular expressions) to specific columns in specific tables. Then, after the data 
have been simulated, you can save them out to a file either in the CSV format or
as a SQL script.
'''
#### SQL lite python library 
#### The Technical Specifications ...are in the code comments ####
''' These code comments follow the pydoc standard. Or at least attempt to. '''

#### Import the Python libraries you’ll need ####
# Unless otherwise specified (e.g. Faker) you can install these 
# modules by running `pip install MOD` where MOD is the name
# of a given module. If you don’t have the `pip` module itself, you 
# can do `easy_install pip`

# Parse configuration files
# https://docs.python.org/2/library/configparser.html
import ConfigParser

# Random number generation and sampling from a list
# https://docs.python.org/2/library/random.html
import random

# Various character string functions and more importantly, variables
# https://docs.python.org/2/library/string.html
import string

# Random name/telephone/email/sentence/etc. etc. etc. generation
# This one you’ll need to install first, as per their website
# https://pypi.python.org/pypi/fake-factory/0.4.0
from faker import Faker
fake = Faker()



# Create in-memory database tables instead of screwing around
# with dictionary objects
# https://docs.python.org/2/library/sqlite3.html
# http://sebastianraschka.com/Articles/sqlite3_database.html
import sqlite3

# Generate random strings that match a given regexp
# https://pypi.python.org/pypi/rstr/2.1.2
import rstr

# If at some point you need to break into the debug interface, you copy-paste in the two
# lines below and uncomment them:
# import pdb
# pdb.set_trace()

def sample_wr(values,nn):
	'''Believe it or not, the standard random library only has sampling without replacement
	but no sampling with replacement. Fine, we’ll write our own, here it is.
	:values:	List of values to sample from with replacement, i.e. they won’t necessarily
				be unique.
	:nn:		Number of values to sample
	'''
	return([random.choice(values) for ii in xrange(nn)])

def simxegers(simxeger,nn):
	'''Just a wrapper for concisely generating an array of “inverted regexps”
	:simxeger:	A regular expression that each generated character string must match.
	:nn:		How many such strings to generate.
	'''
	return([rstr.xeger(simxeger) for ii in xrange(nn)])

def makeunique(func, funarg, nn):
	'''A wrapper that insures that a function which returns an array returns a unique
	array. Note that it’s possible to enter an endless loop where it’s impossible to 
	satisfy the uniqueness condition for a given data type. Might want to think about
	how to detect such loops and exit from them. Might generally be a more elegant
	or concise way to solve this problem. Is maybe this a use case for decorators?
	:func: 		A function that takes :funarg: and :nn: as arguments.
	:funarg:	The argument the function takes (in our case either a simxeger string,
				a simtype string, or an array of values).
	:nn:		How many unique values to return.
	'''
	result = []
	while len(result) < nn:
		result.extend(func(funarg,nn))
		result = list(set(result))
	return(result[:nn])

def simCol(simtype, nn=100, unique=False, values = [], simxeger = ‘’, fracnull = 0):
	'''Return an array of randomly generated values, which can be used as a column in a
	simulated table.
	:simtype: 	The type of values to generate. By default either numeric or string depending
	on the SQL file, but can be overriden by the user to be anything supported
	by the Faker module. If :values: or :simxeger: are specified, then this argument
	is ignored.
	:nn:		The number of values to generate.
	:unique:	Whether the values should all be unique. Particularly useful for primary keys.
	:values:	Values from which the return values should be picked. For example, if values
				is [1,2,3] then this function should return an array that is a random sampling 
				of those two numbers. If :unique: is true, then `len(values) >= nn` should also 
				be true, and otherwise there will be an error, so it’s a good idea to catch this
				condition and return a user friendly error instead of whatever the 
	`random.sample(values,nn)` would return by default. If :simxeger: is specified
	then this argument and :values: are both ignored. The anticipated use for this
	feature is simulating foreign key relationships in the data.
	:simxeger:	A regular expression (regex) that specifies the format of the random string to
				be generated. The point is to give the user an easy way to define a custom
				data type in the config file without having to modify the source code.
	:fracnull:	A number between 0 and 1 inclusive that specifies how many of the returned 
				values should be replaced with NULL (not yet sure how sqlite3 represents
				NULL values but use that format). A lot of the columns contain missing values
				and this allows the user to simulate this.
	'''
	if len(simxeger) > 0:
		'''If a simxeger is specified, just generate a bunch of those and ignore the other stuff'''
		if unique:
			result = makeunique(simxegers, simxeger, nn)
		else:
			result = simxegers(simxeger, nn)
	elif len(values) > 0:
		'''Otherwise, pick from a list'''
		if unique:
			'''remember what was said about catching errors here
			If there are no errors, the below samples nn values WITHOUT replacement.'''
			result = random.sample(values, nn)
		else: 
			result = sample_wr(values, nn)
	else 
		'''If neither of the above apply, we generate a simulated value of a type specified by the
		:simtype: argument. If that argument is missing, give an informative error. Below, is a
		Python equivalent of a case statement. Craaaaazy.

		Okay, so here is the deal with lambda. Lambda allows you to create an anonymous inline 
		function. So, `fn = lambda: print(‘Woohoo’)` will create a function that returns ‘Woohoo’ 
		everytime you call `fn()`. `fn = lambda xx: xx^2` will create a function that returns 81 when 
		you call `fn(9)`. `fn = lambda xx,yy: xx*yy` will create a function that returns 20 when you 
		call `fn(4,5)`. We’re calling this function’s first argument ignore because it will get ignored.
		It’s just there to not break `makeunique`.

		For more information about using dictionaries together with lambdas to simulate 
		switches, look here-- http://blog.simonwillison.net/post/57956755106/switch
		'''
	simfun = {'NUMBER': lambda ignore,nn: [random.randint(0,99999) for ii in xrange(nn)],
				'VARCHAR2': lambda ignore,nn: [rstr.postalsafe(10) for ii in xrange(nn)]		
			}[simtype]
	'''So, in the above code simfun is whichever function is appropriate to the specified data
	type. There are going to be a lot more as we go, many of them from the Faker library. 
	Now that we have a function to use, we generate the result, uniquified if necessary.'''

if unique:
	result = makeunique(simfun, ’ComeWorkAtCIRD’, nn)
else:
	result = simfun(‘ItsAwesomeHere’,nn)

	return(result)

''' Okay, Bob, forgive me for going overboard with the above. I kind of had a flash of inspiration, and ran with it. Don’t worry, though, there is plenty for you to do. For example, the sqlite3 library. 
I’m leaving that one wide open for you. Long story short, it may be more convenient to use that
instead of manually looping over dictionary objects. So the function definitions that would use it
are going to be much less pre-written than the above (which, by the way, should not be treated 
as complete and production-ready functions until you add the missing functionality and test 
them).'''

def readDDL(sqlfiles):
	''' Reads table definitions, foreign keys, and primary keys from one or more SQL files, 
	supplementing them with use-supplied information from optionally one or more config 
	files (handled through ConfigParser). An empty in-memory sqlite database containing 
	empty tables is created from these table definitions and either it or a handle to it 
	(depending on how this is supposed to be done in sqlite3) is returned by this function.
	:sqlfiles:		A list of character strings representing paths to SQL files
	'''

def simTable(sqlitedb, tableName):
	''' Reads a handle (or connection or whatever) to an sqlite in-memory database then 
	uses additional settings obtained from the config file to populate it with random values of 
	the appropriate type. If there are config file settings specifying things like uniqueness, 
	permitted values, or custom data formats, use those and if there aren’t, fall back on the 
	table definitions. In the first iteration, don’t worry about the configs, just let everything be
	a varchar or number. 

	If you use simCol, the first column to be populated (perhaps the primary key) would use 
	an `INSERT` statement, and the rest would be done with an `UPDATE` statement. Or 
	perhaps it might be easier to insert the random data row-wise (and just throw away 
	simCol and instead write e.g. simRow making use of sqlite3 functions).
	:sqlitedb:		A handle (or connection or whatever) to an sqlite database
	:tableName:	A string indicating the name of a table to fill with simulated data
	'''

def simDB(sqlitedb):
	'''I suggest that you first populate tables that don’t have any foreign keys using simTable. 
	Then, keep looping over the remaining tables, skipping the ones whose foreign key 
	dependencies cannot yet be satisfied by the already-created tables, until you either 
	populate them all or some endless loop detector you write causes the program to abort.
	:sqlitedb:	A handle (or connection or whatever) to an sqlite database
	'''

def writeDB(sqlitedb, filename, filetype):
			'''Writes out the contents of an sqlite database either to a CSV file (or files) or to an SQL 
	file. Note, there might already exist functionality for doing this in the sqlite3 library that does this, so it’s a good idea to check the documentation before bothering to write this function. Otherwise …
	:sqlitedb:		A handle (or connection or whatever) to an sqlite database
	:filename:		A string containing a valid path and file name to which the output should be 
	written.
			:filetype:		Either ‘sql’ or ‘csv’. If ‘sql’ then the file should be an (Oracle compatible!) 
	series of `INSERT` statements. If ‘csv’ then a CSV representation of each 
	table. 

#### TBD: a sample config file… but for the first iteration, let not even use a config file
