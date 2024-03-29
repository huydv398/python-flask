import os
from typing import List, Dict
from flask import Flask
import mysql.connector
import json
import logging
import time
import datetime
from mysql.connector import errorcode
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request
from datetime import datetime
from typing import List, Dict
import json

app = Flask(__name__)

config = {
    'user': 'flask',
    'password': 'flask',
    'host': 'db',
    'port': '3306',
    'raise_on_warnings': True,
    'auth_plugin': 'mysql_native_password',
    'database': 'flask'
}
DB_NAME = 'flask'

TABLES = {}

TABLES['tb_student'] = (
    "CREATE TABLE `tb_student` ("
    "  `MSV` int NOT NULL AUTO_INCREMENT,"
    "  `last_name` varchar(50) NOT NULL,"
    "  `birth_date` date NOT NULL,"
    "  `ADDR_BORN` varchar(255) NOT NULL,"
    "  `ADDR` varchar(255) NOT NULL,"
    "  `PHONE` varchar(10) NOT NULL,"
    "  `CCCD` varchar(12) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `hire_date` TIMESTAMP NOT NULL,"
    "  `EMAIL` varchar(255) NOT NULL,"
    "  `Status` INT DEFAULT 1,"
    "  PRIMARY KEY (`MSV`)"
    ") ENGINE=InnoDB")


# #Mở một kết nối đến máy chủ MySQL và lưu trữ đối tượng kết nối trong biến con.
conn = mysql.connector.connect(**config)

# # tạo một con trỏ mới: cursor, theo mặc định là đối tượng MySQLCursor,
# # sử dụng phương thức cursor() của connector.
cursor = conn.cursor()
####------------------------------


app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/user")
def list_user():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    select = """SELECT * FROM tb_student WHERE Status='1'"""
    cursor.execute(select)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("list-user.html", result=result)

@app.route("/user/<param>", methods=['GET', 'POST'])
def edituser(param):
    if request.method == 'GET':
        # return param
        func = "Sửa thông tin Sinh viên"
        conn = mysql.connector.connect(**config)
        action = "{{ url_for('edituser') }}"
        cursor = conn.cursor()
        select = ("SELECT * FROM tb_student WHERE Status='1' AND MSV = " + param)
        cursor.execute(select)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # return result
        return render_template("createuser.html", result=result, func=func, param=param, action=action)
    if ((request.method == 'POST') and (param != 0)):
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        # edit_sinhvien = ("""UPDATE tb_student 
        #                 SET (last_name = %(name)s, birth_date =  %(birthday)s , ADDR =  %(addr1)s, PHONE = %(phonenum)s, gender = %(gender)s, EMAIL = %(email)s, CCCD = %(cccd)s, ADDR_BORN = %(addr2)s, hire_date = %(today)s)
        #                 WHERE MSV = '%(id)s'""")
        # name = request.form['Name']
        edit_sinhvien = ("UPDATE tb_student SET last_name = %(name)s , birth_date =  %(birthday)s , ADDR =  %(addr1)s, PHONE = %(phonenum)s, gender = %(gender)s, EMAIL = %(email)s, CCCD = %(cccd)s, ADDR_BORN = %(addr2)s, hire_date = %(today)s WHERE MSV = %(id)s")
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        data_sinhvien = {
            'name': request.form['Name'],
            'birthday': request.form['birthday'],
            'addr1': request.form['addr'],
            'phonenum': request.form['phonenum'],
            'gender': request.form['gender'],
            'email': request.form['email'],
            'cccd': request.form['cccd'],
            'addr2':request.form['addr_born'],
            'today': timestamp,
            'id': request.form['MSV']
        }
        cursor.execute(edit_sinhvien, data_sinhvien)
        conn.commit()
        cursor.close()
        conn.close()
        return render_template("test.html")
        # return data_sinhvien

@app.route("/createuser", methods=['GET', 'POST'])
def createuser():
    if request.method == 'GET':
        func = "Tạo sinh viên mới"
        action = "/createuser"
        param = ''
        result = [['']]
        # return fun
        return render_template("createuser.html", func=func, result=result, param = '', action=action)
        # return render_template("create-user.html", results_cluster=results_cluster)
    if request.method == 'POST':
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        # #thiết lập chuẩn dữ liệu của DATABASE
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print("Timestamp:", current_timestamp)
        # name = request.form['Name']
        # birthday = request.form['birthday']
        # addr1 = request.form['addr_born']
        
        # phonenum = request.form['phonenum']
        # email = request.form['email']
        # cccd = request.form['cccd']
        # addr2 = request.form['addr']
        # gender = request.form['gender']
        
        add_sinhvien = ("INSERT INTO tb_student "
                        "(last_name, birth_date, ADDR, PHONE, gender, EMAIL, CCCD, ADDR_BORN, hire_date) "
                        "VALUES (%(name)s, %(birthday)s, %(addr1)s, %(phonenum)s, %(gender)s, %(email)s, %(cccd)s, %(addr2)s, %(today)s)")
        # name = request.form['Name']
        
        data_sinhvien = {
            'name': request.form['Name'],
            'birthday': request.form['birthday'],
            'addr1': request.form['addr'],
            'phonenum': request.form['phonenum'],
            'gender': request.form['gender'],
            'email': request.form['email'],
            'cccd': request.form['cccd'],
            'addr2':request.form['addr_born'],
            'today': timestamp
        }
        # test = ("John", "Highway 21")
        # Insert new employee
        # cursor.execute("INSERT INTO tb_student (last_name, birth_date, ADDR, PHONE, gender, EMAIL, CCCD, ADDR_BORN, hire_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (name, birthday, addr2, phonenum, gender, email, cccd, addr1, today))
        cursor.execute(add_sinhvien, data_sinhvien)
        conn.commit()
        cursor.close()
        conn.close()
        return render_template("test.html")
        # return data_sinhvien

@app.route("/deluser", methods=['POST'])    
def deluser():
    if request.method == 'POST':
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        name = request.form['MSV']
        cursor.execute("UPDATE tb_student SET Status = 0 WHERE MSV = " + name)
        conn.commit()
        cursor.close()
        conn.close()
        return render_template("test.html")  
        # return name

@app.route("/test")
def test():
    test = "huydv"
    return render_template("test.html", test = test)


if __name__ == '__main__':
    app.run(host='0.0.0.0')