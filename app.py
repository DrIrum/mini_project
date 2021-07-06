from flask import Flask, render_template, request
from urllib.request import urlopen
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import json
app = Flask(__name__)

engine = create_engine("mysql+pymysql://root:Irum123_@localhost:3306/login")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/irum")
def irum():
    students = db.execute("SELECT * FROM user").fetchone()
    return str(students)
@app.route("/", methods=['GET'])
def index():
    url = "https://cms.mlcs.xyz/api/view/program_sessions/all/"

    response = urlopen(url)

    data_json = json.loads(response.read())

    cs_session = []
    for a in data_json:
        cs_session.append(a['Session_Title'])
    print (cs_session)
    return render_template("index.html", cs_session=cs_session)

@app.route("/user",  methods=['POST'])
def user():
   if request.method=='POST':
    uname = request.form.get("uname")
    password = request.form.get("password")
    print(uname, password)
    db.execute("INSERT into user(user_name, password) VALUES (:user_name, :password)", {"user_name": uname, "password":password})
    db.commit()
    return render_template("user.html" , user=user)
   else:
       return render_template("user.html", user=user)
@app.route("/create",  methods=['POST'])
def create():
    url = "https://cms.mlcs.xyz/api/view/teaching_staff/all/"

    response = urlopen(url)

    data_json = json.loads(response.read())

    teacher_name = []
    for b in data_json:
        teacher_name.append(b['teacher_name'])
    print(teacher_name)

    gname = request.form.get("gname")
    project_title= request.form.get("project_title")
    supervisor=request.form.get("supervisor")
    psw= request.form.get("psw")
   # db.execute("INSERT into project(group_leader_name, project_title, supervisor, members) VALUES (:group_leader_name, :project_title, :supervisor, :psw)",
    #     {"group_leader_name" : gname, "project_title" : project_title, "supervisor" :supervisor, "psw":psw})
    #db.commit()
    return render_template("create.html" , teacher_name=teacher_name, gname=gname, project_title=project_title, supervisor=supervisor,psw=psw)

@app.route("/success",  methods=['POST'])
def success():
    url = "https://cms.mlcs.xyz/api/view/students_of/BSIT-2016/all/"

    response = urlopen(url)

    data_json = json.loads(response.read())

    student_name = []
    for s in data_json:
        student_name.append(s['student_name'])
    print(student_name)
    return render_template("success.html", student_name=student_name)

@app.route("/success2" , methods=['GET', 'POST'])
def success2():

    return render_template("success2.html")

if __name__ == "__main__":
    app.run(debug=True)
