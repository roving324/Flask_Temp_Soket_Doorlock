import serial
import pymysql
from datetime import datetime

global ser
ser = serial.Serial("/dev/ttyACM0",9600)
db_connect = pymysql.connect(host='localhost',db='mydb',user='jun',password='1234',charset='utf8')
db_connected = db_connect.cursor()

PW = ""
while True:
	if ser.readable():
		now = datetime.now()
		date = now.strftime("%Y-%m-%d %H:%M:%S")
		sql = "SELECT pw FROM Doorlock"
		db_connected.execute(sql)
		RPW = db_connected.fetchall()
		RPW = RPW[0][0]
		CPW = "#9"
		sql = "INSERT INTO LoginDoorlockList(pw,flag,date) value(%s,%s,%s)"
		sr = ser.readline()
		PW += sr.decode()[:1]
		if PW == CPW:
			PW = ""
			while True:
				if ser.readable():
					now = datetime.now()
					date = now.strftime("%Y-%m-%d %H:%M:%S")
					sr = ser.readline()
					PW += sr.decode()[:1]
					if len(PW) == 5:
						if PW[-1:] != "*":
							PW = ""
							break
						val = (PW[:4],"changePW",date)
						db_connected.execute(sql,val)
						db_connect.commit()
						sql = "UPDATE Doorlock SET pw = %s, date = %s"
						val = (PW[:4],date)
						db_connected.execute(sql,val)
						db_connect.commit()
						PW = ""
						break
		if len(PW) == 4:
			ser.write(RPW.encode())
			if PW == RPW:
				val = (PW,"success",date)
				db_connected.execute(sql,val)
				db_connect.commit()
				PW = ""
			elif PW != RPW:
				val = (PW,"Fail",date)
				db_connected.execute(sql,val)
				db_connect.commit()
				PW = ""
