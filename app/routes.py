from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, TodoTasks
from app import db
from app.forms import RegistrationForm
from werkzeug.urls import url_parse



@app.route('/index')
@login_required
def index():
    return render_template('index.html')
  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
           flash('Invalid username or password')
           return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        # next_page = request.args.get('next')
        next_page = url_for("temp")
        if not next_page or url_parse(next_page).netloc != '':
           next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/temp",methods=["GET", "POST"])
@app.route("/")
@login_required
def temp():
    if request.method == "GET":
        tasks = TodoTasks.query.filter(TodoTasks.user_id == current_user.id)
        
        return render_template('Home.html', title = "temp", tasks = tasks)
    if request.method ==  "POST":
        data = request.form.get("addTask")
        u = User.query.filter(id == current_user.id)
        print(current_user.id, current_user.username)
        addele = TodoTasks(task = data, user_id = current_user.id)
        db.session.add(addele)
        db.session.commit()
        return redirect(url_for("temp"))
    return "nothing is done"


@app.route('/delete/<int:todo_id>')
@login_required
def delete(todo_id):
    task = TodoTasks.query.get(todo_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("temp")) 

@app.route("/update/<int:todo_id>", methods=["GET","POST"])
@login_required
def update(todo_id):
    if request.method == "GET":
        task_id = TodoTasks.query.get(todo_id)
        return render_template('update.html', task_id = todo_id,task =  task_id.task)

    if request.method == "POST":
        task = request.form.get('updatedTask')
        task_id = TodoTasks.query.get(todo_id)
        task_id.task = task
        db.session.commit()
        return redirect(url_for("temp"))