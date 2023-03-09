import Adafruit_DHT
import pymysql
from flask import Flask, request, render_template
from datetime import datetime

try:
	app = Flask(__name__)
	db_connect = pymysql.connect(host='localhost',db='mydb',user='jun',password='1234',charset='utf8')
	db_connected = db_connect.cursor()
	def Mysql(sql,type = "s",val = ""):
		try:
			if val == "":
				db_connected.execute(sql)
			else:
				db_connected.execute(sql,val)
			if type == "s":
				result = db_connected.fetchall()
				db_connect.commit()
				return result
			elif type == "i":
				db_connect.commit()
		except:
			db_connect.rollback()

	def idread():
		sql = "SELECT id,flag From LoginList ORDER BY date desc LIMIT 1"
		result = Mysql(sql)
		if result[0][1] == "Login":
			return result[0][0]
		else:
			return "Fail"

	@app.route('/',methods=['GET','POST'])
	def Login():
		if request.method == 'POST':
			now = datetime.now()
			date = now.strftime("%Y-%m-%d %H:%M:%S")
			if request.form["submit"] == "로그인":
				id = request.form["id"]
				pw = request.form["pw"]
				sql = "SELECT id FROM user WHERE id = %s AND pw = %s"
				name = Mysql(sql,"s",(id,pw))
				sql = "SELECT COUNT(*) FROM user WHERE id = %s AND pw = %s"
				count = Mysql(sql,"s",(id,pw))
				if len(count) == 0:
					flag = "0"
				else:
					flag = "%s" % count[0]
				sql = "INSERT INTO LoginList(id,flag,date) values(%s,%s,%s)"
				if flag == "0":
					val = (id,"Fail",date)
					Mysql(sql,"i",val)
					return render_template("Login.html",num = flag)
				elif flag == "1":
					val = (id,"Login",date)
					Mysql(sql,"i",val)
					return render_template("Home.html",name = id)
			elif request.form["submit"] == "생성":
				id = request.form["id"]
				pw = request.form["pw"]
				name = request.form["name"]
				sql = "SELECT id FROM user WHERE id = %s"
				count = Mysql(sql,"s",id)
				if len(count) == 1:
					return render_template("Create.html",num = "1")
				sql = "INSERT INTO user(id,pw,name,date) values(%s,%s,%s,%s)"
				val = (id,pw,name,date)
				Mysql(sql,"i",val)
				name = idread()
				if name == "Fail":
					return render_template("Login.html")
				else:
					return render_template("Home.html",name = name)
			elif request.form["submit"] == "취소":
				name = idread()
				if name == "Fail":
					return render_template("Login.html")
				else:
					return render_template("Home.html",name = name)
			elif request.form["submit"] == "Logout":
				sql = "INSERT INTO LoginList(id,flag,date) values(%s,%s,%s)"
				val = (idread(),"Logout",date)
				Mysql(sql,"i",val)
				return render_template("Login.html")
		else:
			name = idread()
			if name == "Fail":
				return render_template("Login.html")
			else:
				return render_template("Home.html",name = name)

	@app.route('/LoginList', methods=['GET','POST'])
	def LoginList():
		name = idread()
		if name == "Fail":
			return render_template("Login.html")
		elif name != "admin":
			return render_template("Home.html",name = name)
		sql = "SELECT * FROM LoginList ORDER BY date desc LIMIT 20"
		rows = Mysql(sql)
		return render_template("LoginList.html",rows = rows,name = name)

	@app.route('/Create', methods=['GET','POST'])
	def Create():
		return render_template("Create.html")

	@app.route('/Home', methods=['GET'])
	def Home():
		name = idread()
		if name == "Fail":
			return render_template("Login.html")
		return render_template("Home.html",name = name)

	@app.route('/TEMP', methods=['GET','POST'])
	def Temp():
		name = idread()
		if name == "Fail":
			return render_template("Login.html")
		sql = "SELECT Temp,Humi,date FROM Tmp ORDER BY date desc LIMIT 1"
		rows = Mysql(sql)
		sql = "SELECT day FROM Tmp GROUP BY day ORDER BY day desc"
		day = Mysql(sql)
		rowList = ()
		for i in day:
			sql = "SELECT Temp,Humi,date FROM Tmp WHERE day = %s ORDER BY date desc LIMIT 1"
			if len(rowList) > 10:
				contiue;
			rowList += Mysql(sql,"s",i)
		return render_template("Temp.html",rows = rows,rowList = rowList,name = name)

	@app.route('/Doorlock', methods=['GET'])
	def Doorlock():
		name = idread()
		if name == "Fail":
			return render_template("Login.html")
		sql = "SELECT * FROM LoginDoorlockList ORDER BY date desc LIMIT 20"
		rows = Mysql(sql)
		return render_template("Doorlock.html",rows = rows,name = name)

	if __name__== '__main__':
		app.run(host = "0.0.0.0",port="3169",debug=True)

finally:
	db_connect.close()
