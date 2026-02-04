from flask import Flask, render_template,request,redirect,url_for,session
import firebase_admin
from  firebase_admin import credentials,db
import os

firebase_config = {
    "type": "service_account",
    "project_id": os.environ["FIREBASE_PROJECT_ID"],
    "private_key_id": os.environ["FIREBASE_PRIVATE_KEY_ID"],
    "private_key": os.environ["FIREBASE_PRIVATE_KEY"].replace("\\n", "\n"),
    "client_email": os.environ["FIREBASE_CLIENT_EMAIL"],
    "client_id": os.environ["FIREBASE_CLIENT_ID"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ["FIREBASE_CLIENT_CERT_URL"]
}


cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred,{"databaseURL":"https://to-do-list-cfcb3-default-rtdb.firebaseio.com/"})


#make an app
ref=db.reference("users")
app=Flask(__name__)
app.secret_key="user"
todolist=[]
todoitem={}
count=1


#specify the route
@app.route("/",methods=["GET","POST"])
def homepage():
 username=session.get("username","")
 if request.method=="POST" and "username" in request.form:
  username=request.form.get("username")
  session["username"]=username
 #global count
 if request.method=="POST" and "Input1" in request.form:
    usertask=request.form["Input1"]
    print(usertask)
    #todoitem={"id":count,"task":usertask}
    #todolist.append(todoitem)
    #count+=1
    username=session.get("username")
    print(username)
    ref.child(username).child("todolist").push(usertask)
 if request.method=="POST" and "logout" in request.form:
    username=None
    return render_template("index.html",htmltask=[],htmluser=username)
 task = {}

 if username:
    user_data = ref.child(username).get()

    if user_data and "todolist" in user_data:
        task = user_data["todolist"]
        print(task)
    else:
        task = {}

 return  render_template("index.html",htmltask=task,htmluser=username) #sending data to html
@app.route("/delete/<string:taskid>")
def deletepage(taskid):
   print(taskid)
   username=session.get("username")
   if username and taskid :
      ref.child(username).child("todolist").child(taskid).delete()
   # print(todolist)
   # for eachdictionary in todolist:
   #    if taskid==eachdictionary["id"]:
   #       ind=todolist.index(eachdictionary)
   #       todolist.pop(ind)
   return redirect(url_for("homepage"))






if "__main__"==__name__:
    app.run(debug=True)



