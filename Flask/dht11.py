import Adafruit_DHT
import pymysql
import time
from datetime import datetime

dht = Adafruit_DHT.DHT11

dhtPin = 14
db_connect = pymysql.connect(host='localhost',db = 'mydb',user='jun',password='1234',charset ='utf8',cursorclass=pymysql.cursors.DictCursor)
db_connected = db_connect.cursor()
try:
	while True:
		humi, temp = Adafruit_DHT.read_retry(dht, dhtPin)
		if humi is not None and temp is not None:
			now = datetime.now()
			current_time = now.strftime("%Y-%m-%d %H:%M:%S")
			day_time = now.strftime("%Y-%m-%d")
			print("Temp=%.1fC Humi=%.1f%% Date=%s" % (temp, humi,current_time))
			sql = "INSERT INTO Tmp (Temp,Humi,date,day) VALUES(%s,%s,%s,%s)"
			db_connected.execute(sql,('%.1fC' % temp,'%.1f%%' % humi,current_time,day_time))
			db_connect.commit()
		time.sleep(1)
except KeyboardInterrupt:
	db_connect.close()
