from werkzeug.exceptions import BadRequestKeyError
from flaskServer import app
from flask import json, render_template, request, jsonify, redirect, abort
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






@app.route('/signup')
def signup():
    if current_user.is_authenticated:
        return redirect('/userhome')
    return render_template('signUp.html')

@app.route('/newUser', methods = ['POST'])
def newUser():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    result = db.addUser(username, email, password)
    print(email, username, password)
    print('adding new user', result)
    return jsonify(result = result)



@app.route('/')
@app.route('/signin')
def signin():
    if current_user.is_authenticated:
        return redirect('/userhome')
    return (render_template('stocksimulator.html'))

@app.route('/authenticate', methods = ['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    result = db.authenticate(username, password)
    print(username, password)
    print('logging in', result)
    if type(result) == str:
        return jsonify(result = result)
    else:
        login_user(result)
        return jsonify(result = 'success')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')



@app.route('/userhome/<username>')
def userhome(username):
    print('\n\n\n\n\n\n\n-----------------------------------------------------------------------', username, '\n\n\n\n\n\n\n\n\n')
    return render_template('homepage.html')

@app.route('/addWatchList', methods = ['POST'])
def addWatchList():
    username = request.form['username']
    symbol = request.form['symbol']
    # result = db.addToWatchList(username, symbol)
    # stockStats = db.getStockInfo(symbol)
    return jsonify(result = 'success', stock = {'price': 131.96, 'change': '-5.13 (-3.74%)', 'symbol': 'AAPL'})


<<<<<<< HEAD
@app.route('/getWatchList/<username>', methods = ['GET'])
def getWatchList(username):
    # return jsonify(watchList = db.getWatchList(username))
    return jsonify(result = [{'symbol': 'AAPL', 'price': 131.96, 'change': '-5.13 (-3.74%)'}, {'symbol': 'GOOG', 'price': 1835.74, 'change': '-27.37 (-1.47%)'}, {'symbol': 'AMZN', 'price': 3206.2, 'change': '-31.42 (-0.97%)'}])
=======
@app.route('/getWatchList', methods = ['POST'])
def getWatchList():
    username = request.form['username']
    return jsonify(watchList = db.getWatchList(username))
>>>>>>> 67d2f6560a28bb6076b17f0050600d82078e251b

@app.route('/removeWatchList', methods = ['POST'])
def removeWatchList():
    username = request.form['username']
    symbol = request.form['symbol']
    result = db.removeFromWatchList(username, symbol)
    return jsonify(result = result)


@app.route('/buyStock', methods = ['POST'])
def buyStock():
    username = request.form['username']
    symbol = request.form['symbol']
    share = request.form['share']
    result = db.buyStock(username, symbol, share)
    balence = db.getBalence(username)
    return jsonify(result = result, balence = balence)







@app.route('/portfolio/<username>')
def portfolio(username):
    return render_template('Portfolio.html')

@app.route('/getOwnedStock', methods = ['POST']) 
def getOwnedStock():
    username = request.form['username']
    result = db.getOwnedStock(username=username)
    return jsonify(result = result)
    # return jsonify(result = { 'stocks': [{ 'symbol': 'AAPL', 'price': 131.96, 'share': 4, 'value': 527.84 }, { 'symbol': 'GOOG', 'price': 1835.74, 'share': 3, 'value': 5507.22 }, { 'symbol': 'GOOG', 'price': 1835.74, 'share': 3, 'value': 5507.22 }, { 'symbol': 'GOOG', 'price': 1835.74, 'share': 3, 'value': 5507.22 }], 'totalValue': 6035.06 })

@app.route('/sellStock', methods = ['POST'])
def sellStock():
    username = request.form['username']
    symbol = request.form['symbol']
    share = request.form['share']
    result = db.buyStock(username, symbol, share)
    balence = db.getBalence(username)
    stockInfo = db.getSingleStockOwned(username, symbol)
    return jsonify(result = result, balence = balence, stock = stockInfo)



@app.route('/balence/<username>', methods = ['POST'])
def balence(username):
    return jsonify(result = db.getBalence(username))