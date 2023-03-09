# Flask_Temp_Soket_Doorlock
<img src="https://github.com/roving324/Flask_Temp_Soket_Doorlock/blob/main/Flask/img/Login.PNG">
<img src="https://github.com/roving324/Flask_Temp_Soket_Doorlock/blob/main/Flask/img/Create.PNG">
<img src="https://github.com/roving324/Flask_Temp_Soket_Doorlock/blob/main/Flask/img/Admin_Home.PNG">
<img src="https://github.com/roving324/Flask_Temp_Soket_Doorlock/blob/main/Flask/img/Home.PNG">
<img src="https://github.com/roving324/Flask_Temp_Soket_Doorlock/blob/main/Flask/img/Temp.PNG">
<img src="https://github.com/roving324/Flask_Temp_Soket_Doorlock/blob/main/Flask/img/Doorlock.PNG">
<img src="https://github.com/roving324/Flask_Temp_Soket_Doorlock/blob/main/Flask/img/LoginList.PNG">

## 관리자 전용 로그인 기록 확인
### Python
```
def LoginList():
 name = idread()
 if name == "Fail":
 	return render_template("Login.html")
 elif name != "admin":
 	return render_template("Home.html",name = name)
 sql = "SELECT * FROM LoginList ORDER BY date desc LIMIT 20"
 rows = Mysql(sql)
 return render_template("LoginList.html",rows = rows,name = name)
```
### Html <script>
```
if("{{name}}" != "admin"){
  document.getElementById("Login").style.visibility='hidden'
}
```

## TEMP
	
### Temp 현재,일자별 데이터 조회
```
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
```

### Flask 변수 html에 테이블로 표현
```
<table border="1">
  <tr>
  <td><center>온도</center></td>
  <td><center>습도</center></td>
  <td><center>일시</center></td>
  </tr>
  {% for value in rows %}
  <tr> 
  <td>&nbsp;{{value[0]}}&nbsp;</td>
  <td>&nbsp;{{value[1]}}&nbsp;</td>
  <td>&nbsp;{{value[2]}}&nbsp;</td>
  </tr>
  {% endfor %}
</table>
```

## PW 최소글자 수, 필수 입력
```
<td>패스워드</td><td>:</td>
<td><input type="password" id="pw" name="pw" minlength="4" required></td>
```

## body 화면 중앙 배치
```
body{
 display: flex;
 justify-content: center;
 align-items: center;
 }
```

## ID 확인
```
name = idread()
  if name == "Fail":
    return render_template("Login.html")
  else:
    return render_template("Home.html",name = name)
```

## 도어락 데이터 기록 및 아두이노 연결
```
import serial
ser = serial.Serial("/dev/ttyACM0",9600)
sr = ser.readline()
PW += sr.decode()[:1]
```
