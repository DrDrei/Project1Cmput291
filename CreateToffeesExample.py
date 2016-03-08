# Note: Python does not have an auto commit. Thus, commit at the end of each statement is important.
# python3 CreateToffees.py
# File from introduction to cx_oracle



import sys
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it



def createTable():
	
	# get username
	user = input("Username [%s]: " % getpass.getuser())
	if not user:
    		user=getpass.getuser()
	
	# get password
	pw = getpass.getpass()

	# The URL we are connnecting to
	conString = '' + user + '/' + pw +'@gwynne.cs.ualberta.ca:1521/CRS'
	
	# SQL statement to execute
	createStr = ("create table TOFFEES "
	"(T_NAME VARCHAR(32) PRIMARY KEY, SUP_ID INTEGER, PRICE FLOAT, SALES INTEGER, TOTAL INTEGER)")
	
	try:
		# Establish a connection in Python
		connection = cx_Oracle.connect(conString)
		cursor = connection.cursor()
		dropTables(conString)
		createTables(conString)
		# try:
		# 	for drop in dropTables:
		# 		cursor.execute(drop)
		# 	for table in createTables:
		# 		cursor.execute(table)
		# except:
		# 	for table in createTables:
		# 		cursor.execute(table)
		
		# data = [('Quadbury', 101, 7.99, 0, 0), ('Smarties',102,6.99,1,2)]

		# cursor.bindarraysize = 2
		# cursor.setinputsizes(32, int, float, int, int)
		# cursor.executemany("INSERT INTO TOFFEES(T_NAME, SUP_ID, PRICE, SALES, TOTAL) "
  #                                   "VALUES (:1, :2, :3, :4, :5)", data)
		# curs.execute("INSERT INTO TOFFEES "
		# "VALUES('Quadbury',101,7.99,0,0)")
		connection.commit()
		
		# executing a query
		# cursor.execute("SELECT * from people")
		# get all data and print it
		# rows = cursor.fetchall()
		# for row in rows:
		# 	print(row)
		
		# getting metadata
		# rows = cursor.description
		# columnCount = len(rows)

		# display column names and type
		# (name, type, display_size,internal_size,precision,scale,null_ok)
		# for row in rows:
		# 	print(row[0]," ",row[1])

		# close the connection
		cursor.close()
		connection.close()

	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)

def dropTables(connectionStr):
	try:
		connection = cx_Oracle.connect(connectionStr)
		cursor = connection.cursor()
		
		dropTablesArr = [
				  "DROP TABLE owner",
				  "DROP TABLE auto_sale",
				  "DROP TABLE restriction", 
				  "DROP TABLE driving_condition", 
				  "DROP TABLE ticket", 
				  "DROP TABLE ticket_type", 
				  "DROP TABLE vehicle", 
				  "DROP TABLE vehicle_type", 
				  "DROP TABLE drive_licence", 
				  "DROP TABLE people"]
		for table in dropTablesArr:
			try:
				cursor.execute(table)
			except:
				print("Failed: ", table)

		connection.commit()

	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)

def createTables(connectionStr):
	try:
		connection = cx_Oracle.connect(connectionStr)
		cursor = connection.cursor()


		createTables = [("CREATE TABLE people ""(sin CHAR(15), name VARCHAR(40), height number(5,2), weight number(5,2), eyecolor VARCHAR (10), haircolor VARCHAR(10), addr VARCHAR2(50), gender CHAR, birthday DATE, PRIMARY KEY (sin), CHECK (gender IN ('m', 'f')))"), 
						("CREATE TABLE drive_licence ""(licence_no CHAR(15), sin CHAR(15), class VARCHAR(10), photo BLOB, issuing_date DATE, expiring_date DATE, PRIMARY KEY (licence_no), UNIQUE (sin), FOREIGN KEY (sin) REFERENCES people ""ON DELETE CASCADE)"),
						("CREATE TABLE driving_condition ""(c_id INTEGER, description VARCHAR(1024), PRIMARY KEY (c_id))"),
						("CREATE TABLE restriction ""(licence_no CHAR(15), r_id INTEGER, PRIMARY KEY (licence_no, r_id), FOREIGN KEY (licence_no) REFERENCES drive_licence, FOREIGN KEY (r_id) REFERENCES driving_condition)"),
						("CREATE TABLE vehicle_type ""(type_id integer, type CHAR(10), PRIMARY KEY (type_id))"),
						("CREATE TABLE vehicle ""(serial_no CHAR(15), maker VARCHAR(20), model VARCHAR(20), year number(4,0), color VARCHAR(10), type_id integer, PRIMARY KEY (serial_no),FOREIGN KEY (type_id) REFERENCES vehicle_type)"),
						("CREATE TABLE owner ""(owner_id CHAR(15), vehicle_id CHAR(15), is_primary_owner CHAR(1), PRIMARY KEY (owner_id, vehicle_id), FOREIGN KEY (owner_id) REFERENCES people, FOREIGN KEY (vehicle_id) REFERENCES vehicle, CHECK (is_primary_owner IN ('y', 'n')))"),
						("CREATE TABLE auto_sale ""(transaction_id int, seller_id CHAR(15), buyer_id CHAR(15), vehicle_id CHAR(15), s_date date, price numeric(9,2), PRIMARY KEY (transaction_id), FOREIGN KEY (seller_id) REFERENCES people, FOREIGN KEY (buyer_id) REFERENCES people, FOREIGN KEY (vehicle_id) REFERENCES vehicle)"),
						("CREATE TABLE ticket_type ""(vtype CHAR(10), fine number(5,2), PRIMARY KEY (vtype))"),
						("CREATE TABLE ticket ""(ticket_no int, violator_no CHAR(15), vehicle_id CHAR(15), office_no CHAR(15), vtype char(10), vdate date, place varchar(20), descriptions varchar(1024), PRIMARY KEY (ticket_no), FOREIGN KEY (vtype) REFERENCES ticket_type, FOREIGN KEY (violator_no) REFERENCES people ON DELETE CASCADE, FOREIGN KEY (vehicle_id) REFERENCES vehicle, FOREIGN KEY (office_no) REFERENCES people ON DELETE CASCADE)")]

		for table in createTables:
			try: 
				cursor.execute(table)
			except:
				print("Failed: ", table)

		connection.commit()

	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)

if __name__ == "__main__":
    createTable()
