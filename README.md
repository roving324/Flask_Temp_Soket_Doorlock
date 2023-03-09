# Flask_Temp_Soket_Doorlock
<img src="https://github.com/roving324/Flask_Temp_Soket_Doorlock/blob/main/Flask/img/Login.PNG">
<img src="https://github.com/roving324/Flask_Temp_Soket_Doorlock/blob/main/Flask/img/Create.PNG">
<img src="https://github.com/roving324/Flask_Temp_Soket_Doorlock/blob/main/Flask/img/Admin_Home.PNG">
<img src="https://github.com/roving324/Flask_Temp_Soket_Doorlock/blob/main/Flask/img/Home.PNG">
<img src="https://github.com/roving324/Flask_Temp_Soket_Doorlock/blob/main/Flask/img/Temp.PNG">
<img src="https://github.com/roving324/Flask_Temp_Soket_Doorlock/blob/main/Flask/img/Doorlock.PNG">
<img src="https://github.com/roving324/Flask_Temp_Soket_Doorlock/blob/main/Flask/img/LoginList.PNG">

```
if("{{name}}" != "admin"){
  document.getElementById("Login").style.visibility='hidden'
}
```

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

```
<td>패스워드</td><td>:</td>
<td><input type="password" id="pw" name="pw" minlength="4" required></td>
```

```
body{
 display: flex;
 justify-content: center;
 align-items: center;
 }
```

```
name = idread()
  if name == "Fail":
    return render_template("Login.html")
  else:
    return render_template("Home.html",name = name)
```

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
