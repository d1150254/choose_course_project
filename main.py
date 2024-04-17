# coding=utf-8
# -*- coding: UTF-8 -*-
from flask import Flask, request, render_template, redirect, url_for
import MySQLdb
import data

#建立與SQL資料庫的連線
def getsql():
    return MySQLdb.connect(host="127.0.0.1",user="test",passwd="12345",db="testdb")

#回傳資料庫根據query回傳的table，回傳的格式是tuple
def get_sql_data(query)->tuple:
    connect_sql=getsql()
    cursor=connect_sql.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#將更新的SQL指令傳到資料庫中
def update_sql_data(query)->None:
    connect_sql=getsql()
    cursor=connect_sql.cursor()
    cursor.execute(query)
    connect_sql.commit()

#判斷輸入的帳號密碼正不正確
def check_sql_account(username,password)->bool:
    query = "SELECT passwd FROM account where studentId='{}';".format(username)
    res_passwd_sql=get_sql_data(query)
    return password==res_passwd_sql[0][0]

#判斷能不能加選 0->可以 1->不同系的課 2->課堂滿了 3->有衝堂 4->有重名課程 5->超過學分限制(30) 6->錯誤的選課代號
def check_add_course(username, courseid)->int:
    query = "SELECT department FROM course where id='{}';".format(courseid)
    course_department=get_sql_data(query)
    query = "SELECT department FROM student where id='{}';".format(username)
    student_department=get_sql_data(query)

    query = "SELECT maxstudent, nowstudent FROM course where id='{}';".format(courseid)
    course_student_count=get_sql_data(query)

    query = "SELECT courseid FROM schedule where studentid='{}';".format(username)
    user_all_course=get_sql_data(query)
    query = "SELECT coursetime FROM course where id='{}';".format(courseid)
    course_time=get_sql_data(query)
    user_all_course_time=[]
    for i in user_all_course:
        query = "SELECT coursetime FROM course where id='{}';".format(i[0])
        user_all_course_time.append(get_sql_data(query)[0][0])

    query = "SELECT coursename FROM course where id='{}';".format(courseid)
    course_name=get_sql_data(query)
    user_all_course_name=[]
    for i in user_all_course:
        query = "SELECT coursename FROM course where id='{}';".format(i[0])
        user_all_course_name.append(get_sql_data(query)[0][0])

    query = "SELECT credit FROM student where id='{}';".format(username)
    user_crecit=get_sql_data(query)
    query = "SELECT credit FROM course where id='{}';".format(courseid)
    course_credit=get_sql_data(query)
    
    if(len(course_department)==0):
        return 6
    elif(course_department[0][0]!=student_department[0][0]): 
        return 1
    elif(course_student_count[0][0]<=course_student_count[0][1]):
        return 2
    elif(course_time[0][0] in user_all_course_time):
        return 3
    elif(course_name[0][0] in user_all_course_name):
        return 4
    elif(user_crecit[0][0]+course_credit[0][0]>30):
        return 5
    return 0

#判斷能不能退選 0->可以 1->不存在課表中的課 2->退選完學分小於9學分 3->要退的是必修課
def check_drop_course(username, courseid)->int:
    query = "SELECT studentid, courseid FROM schedule where studentid='{}' and courseid={};".format(username,courseid)
    if(len(get_sql_data(query))==0):
        return 1
    
    query = "SELECT credit FROM student where id='{}';".format(username)
    user_credit=get_sql_data(query)[0][0]
    query = "SELECT credit FROM course where id='{}';".format(courseid)
    course_credit=get_sql_data(query)[0][0]

    query = "SELECT compulsory FROM course where id='{}';".format(courseid)
    compulsory=get_sql_data(query)[0][0]

    if(user_credit-course_credit<9):
        return 2
    elif(compulsory==1):
        return 3
    return 0

#加選更新
def add_course(username,courseid)->None:
    query_update=[]
    #更新course選課人數
    query = "SELECT nowstudent FROM course where id='{}';".format(courseid)
    course_nowstudent=get_sql_data(query)[0][0]
    course_nowstudent+=1
    query_update.append("UPDATE course SET nowstudent = {} WHERE course.id = '{}'".format(course_nowstudent,courseid))

    #更新學生學分
    query = "SELECT credit FROM course where id='{}';".format(courseid)
    course_credit=get_sql_data(query)[0][0]
    query = "SELECT credit FROM student where id='{}';".format(username)
    user_credit=get_sql_data(query)[0][0]
    user_credit+=course_credit
    query_update.append("UPDATE student SET credit = {} WHERE student.id = '{}'".format(user_credit,username))

    #更新schedule
    query_update.append("insert into schedule(studentId, courseId) values('{}','{}')".format(username,courseid))

    for i in query_update:
        update_sql_data(i)

#退選更新
def update_drop_course(username, courseid)->None:
    query_update=[]
    query = "SELECT nowstudent FROM course where id='{}';".format(courseid)
    course_nowstudent=get_sql_data(query)[0][0]-1
    query_update.append("UPDATE course SET nowstudent = {} WHERE course.id = '{}'".format(course_nowstudent,courseid))

    query = "SELECT credit FROM course where id='{}';".format(courseid)
    course_credit=get_sql_data(query)[0][0]
    query = "SELECT credit FROM student where id='{}';".format(username)
    user_credit=get_sql_data(query)[0][0]
    user_credit-=course_credit
    query_update.append("UPDATE student SET credit = {} WHERE student.id = '{}'".format(user_credit,username))

    query = "SELECT id FROM schedule where studentid='{}' and courseid='{}';".format(username,courseid)
    schedule_id=get_sql_data(query)[0][0]
    query_update.append("DELETE FROM schedule where schedule.id='{}'".format(schedule_id))

    for i in query_update:
        update_sql_data(i)

#確認學生帳號有沒有預選必修課了
def check_account_init(username)->bool:
    query = "SELECT check_init FROM student where id='{}';".format(username)
    return get_sql_data(query)[0][0]==1

#幫每個學生帳號預選必修課
def account_init(username)->None:
    print("init")
    query = "SELECT department FROM student where id='{}';".format(username)
    user_department=get_sql_data(query)[0][0]
    query = "SELECT id FROM course where department='{}' and compulsory='{}';".format(user_department,1)
    user_compulsory=get_sql_data(query)
    for courseid in user_compulsory:
        add_course(username,courseid[0])
    query = "UPDATE student SET check_init = {} WHERE student.id = '{}'".format(1,username)
    update_sql_data(query)
    
def showcourse(username):
    query = "SELECT courseid FROM schedule where studentId='{}';".format(username)
    user_course=list(i[0] for i in get_sql_data(query))
    query = "SELECT courseid FROM schedule where studentId='{}';".format(username)
    user_course_time_name=[]

    for i in user_course:
        query = "SELECT coursetime, coursename FROM course where id='{}';".format(i)
        temp=get_sql_data(query)[0]
        user_course_time_name.append([str(temp[0]),str(i)+" "+temp[1]])
    for i in data.class_time_table:
        for num in range(1,6):
            data.class_schedule[i][num]="空堂"

    for i in user_course_time_name:
        for j in range(int(i[0][1]),int(i[0][2])+1):
            data.class_schedule[data.class_time_table[j-1]][int(i[0][0])]=i[1]
        
    return render_template('mainpage.html',weekday=data.weekday, schedule=data.class_schedule)

app = Flask(__name__)

username=""
courseid=""

@app.route('/')
def index():
    global username
    username=""
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    global username
    username=request.form['username']
    password=request.form['password']

    if check_sql_account(username,password) is True:
        if(check_account_init(username) is False):
            account_init(username)
        return redirect(url_for('choose'))
    else:
        return render_template('index.html', error='Invalid username or password')

@app.route('/choose')
def choose():
    global username
    return showcourse(username)

@app.route('/addcourse')
def addcourse():
    return render_template('addcourse.html')

@app.route('/addcourse/check', methods=['POST'])
def addcoursecheck():
    global username
    courseid=request.form['courseid']
    switch=check_add_course(username,courseid)
    if(switch==1):
        return render_template('addcourse.html',error='不能選別系的課程')
    elif(switch==2):
        return render_template('addcourse.html',error='課堂人數已滿')
    elif(switch==3):
        return render_template('addcourse.html',error='有衝堂')
    elif(switch==4):
        return render_template('addcourse.html',error='課表中有同名課程')
    elif(switch==5):
        return render_template('addcourse.html',error='超過學分最高限制(30)')
    elif(switch==6):
        return render_template('addcourse.html',error='錯誤的選課代碼')
    
    add_course(username,courseid)
    return render_template('addcourse.html',success='登記成功')

@app.route('/dropcourse')
def dropcourse():
    return render_template('dropcourse.html')

@app.route('/dropcourse/check',methods=['POST'])
def dropcoursecheck():
    global username
    global courseid
    courseid=request.form['courseid']
    switch=check_drop_course(username,courseid)
    if(switch==1):
        return render_template('dropcourse.html',error='這堂課不存在你的課表中')
    elif(switch==2):
        return render_template('dropcourse.html',error='退選失敗 學分小於9學分')
    elif(switch==3):
        return redirect(url_for('dropcoursecheckdoubelcheck'))
    else:
        return redirect(url_for('dropcoursesuccess'))

@app.route('/dropcourse/check/doubelcheck')
def dropcoursecheckdoubelcheck():
    return """
            <p>這堂課是必修，你確定要退選嗎<p>
            <p><a href="/dropcourse/success">確定</a></p>
            <p><a href="/drawcourse">取消</a></p>
           """

@app.route('/dropcourse/success')
def dropcoursesuccess():
    global courseid
    update_drop_course(username,courseid)
    return render_template('dropcourse.html',success='退選成功')

app.run()