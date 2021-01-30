from flaskServer import app
from flask import render_template, request, jsonify, redirect, abort
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
import db

app.config['SECRET_KEY'] = 'hahahhaha'

# need to do all the db functions

loginManager = LoginManager()
loginManager.init_app(app)

@loginManager.user_loader
def load_user(user_id):
    user = db.getFromId(user_id)
    if type(user) == str:
        return None
    return user
    
@loginManager.unauthorized_handler
def unauthorized():
    return redirect('/')




@app.errorhandler(404)
def page_not_found(e):
    print(str(e))
    return (render_template('404.html'), 404)


@app.route('/checkStatus')
def checkStatus():
    if current_user.is_authenticated:
        return jsonify(status = True)
    else:
        return jsonify(status = False)






@app.route('/')
@app.route('/signup')
def signup():
    if current_user.is_authenticated:
        return redirect('/userhome')
    return render_template('signup.html')

@app.route('/newUser', methods = ['POST'])
def newUser():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    result = db.addUser(username, email, password)
    return jsonify(result = result)




@app.route('/signin')
def signin():
    if current_user.is_authenticated:
        return redirect('/userhome')
    return (render_template('signin.html'))

@app.route('/authenticate', methods = ['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    result = db.authenticate(username, password)
    if type(result) == str:
        return jsonify(result = result)
    else:
        login_user(result)
        return jsonify(result = 'success')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')



@app.route('/userhome')
@login_required
def userhome():
    return render_template('userhome.html')
