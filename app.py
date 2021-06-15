from flask import Flask, render_template, request, session, redirect, url_for
import pyrebase
from oauth2client.client import Error
from configData import config

app = Flask(__name__)
app.secret_key = "kanban-tasker-flask-432"

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

task_hierarchy = ["todo","progress","review","done"]

@app.route('/',methods=['GET','POST'])
def authPage():
    if 'user' in session :
            return redirect(url_for('kanban_tasker'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        yunik = email.replace('@','').replace('.','')
        idToken = None
        try:
            sign_user = auth.sign_in_with_email_and_password(email,password)
            idToken = sign_user['idToken']
            session['user'] = idToken
            session['idDb'] = yunik
            return redirect(url_for('kanban_tasker'))
        except:
            print("Error")
            return render_template("index.html",login_error="Your credentials are incorrect. Please try again.")
    return render_template("index.html")

@app.route('/signup',methods=['GET','POST'])
def signup():
    if 'user' in session :
            return redirect(url_for('kanban_tasker'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        yunik = email.replace('@','').replace('.','')
        try:
            newUser = auth.create_user_with_email_and_password(email,password)
            sign_user = auth.sign_in_with_email_and_password(email,password)
            idToken = sign_user['idToken']
            data = {
                "name" : name
            }
            print(data)
            db.child("users").child(yunik).set(data)
            session['user'] = idToken
            session['idDb'] = yunik
            return redirect(url_for('kanban_tasker'))
        except Error as e:
            print("Could not create account")
    return render_template("signup.html")

@app.route('/tasks')
def kanban_tasker():
    if 'user' in session :
        todo,progress,review,done = [],[],[],[]
        dets = dict(db.child("users").child(session["idDb"]).get().val())
        if 'usertasks' in dets:
            tasks = list(dets['usertasks'].values())
            print(tasks)
            for task in tasks:
                if task['type'] == 'todo':
                    todo.append(task)
                if task['type'] == 'progress':
                    progress.append(task)
                if task['type'] == 'review':
                    review.append(task)
                if task['type'] == 'done':
                    done.append(task)
        mappedTasks = {
            "todo" : todo,
            "progress" : progress,
            "review" : review,
            "done" : done
        }
        return render_template("kanbantasker.html",tasks=mappedTasks,name=dets['name'],pending=len(todo))
    else:
        return redirect(url_for('authPage'))

@app.route('/propagate/<taskid>')
def propagate(taskid):
    if 'user' in session :
        dets = dict(db.child("users").child(session["idDb"]).get().val())
        allIds = list(dets['usertasks'].keys())
        tasks = list(dets['usertasks'].values())
        print(allIds,tasks,taskid)
        #Find in which category the task is
        taskDetails = [(task['type'],tasks.index(task)) for task in tasks if task['id'] == int(taskid)][0]
        print(taskDetails)
        prev_task_type, taskIndex = taskDetails[0],taskDetails[1]
        print(prev_task_type,taskIndex)
        new_task_type = task_hierarchy[task_hierarchy.index(prev_task_type)+1]
        print   
        #Update in the dictionary
        db.child("users").child(session["idDb"]).child('usertasks').child(allIds[taskIndex]).update({"type" : new_task_type})
        return redirect(url_for('kanban_tasker'))
    else:
        return redirect(url_for('authPage'))

@app.route('/delete/<taskid>')
def delete(taskid):
    if 'user' in session :
        dets = dict(db.child("users").child(session["idDb"]).get().val())
        allIds = list(dets['usertasks'].keys())
        tasks = list(dets['usertasks'].values())
        db.child("users").child(session["idDb"]).child('usertasks').child(allIds[tasks.index([task for task in tasks if task['id'] == int(taskid)][0])]).remove()
        return redirect(url_for('kanban_tasker'))
    else:
        return redirect(url_for('authPage'))

@app.route('/addtask/<tasktype>',methods=['GET','POST'])
def addTask(tasktype):
    if 'user' in session :
        dets = dict(db.child("users").child(session["idDb"]).get().val())
        if 'usertasks' in dets:
            tasks = dets['usertasks']
        else:
            tasks = []
        if request.method == 'POST':
            db.child("users").child(session["idDb"]).child("usertasks").push(
                {
                    "id" : len(tasks) + 1,
                    "type" : tasktype,
                    "name" : request.form['title'],
                    "desc" : request.form['desc']
                }
            )
            return redirect(url_for('kanban_tasker'))
        elif tasktype == 'todo':
            taskType = "to-do"
        elif tasktype == 'progress':
            taskType = 'in-progress'
        else:
            taskType = tasktype
        return render_template('addtask.html',tasktype=taskType,act=tasktype)
    else:
        return redirect(url_for('authPage'))

@app.route('/logout')
def logout():
    if 'user' in session :
        session.pop("user",None)
        return redirect(url_for('authPage'))
    else:
        return redirect(url_for('authPage'))

if __name__ == '__main__':
    app.run(debug=True)