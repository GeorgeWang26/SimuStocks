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
    print('\n\n\n\n\n\n\n-----------------------------------------------------------------------\n', username, '\n\n\n\n\n\n\n\n\n')
    return render_template('homepage.html')


@app.route('/getWatchList', methods = ['POST'])
def getWatchList():
    db.updateAllStockInfo()
    username = request.form['username']
    print('\n\n\n\n\n\n\n-----------------------------------------------------------------------\n', username, '\n\n\n\n\n\n\n\n\n')
    watchList = db.getWatchList(username)
    print('\n\n\n\n\n\n\n-----------------------------------------------------------------------\n', watchList, '\n\n\n\n\n\n\n\n\n')
    return jsonify(result = watchList)
    # return [{'symbol': 'AAPL', 'price': 131.96, 'change': '-5.13 (-3.74%)'}, {'symbol': 'GOOG', 'price': 1835.74, 'change': '-27.37 (-1.47%)'}, {'symbol': 'AMZN', 'price': 3206.2, 'change': '-31.42 (-0.97%)'}]


@app.route('/addWatchList', methods = ['POST'])
def addWatchList():
    username = request.form['username']
    symbol = request.form['symbol']
    result = db.addToWatchList(username, symbol)
    stockStats = db.getStockInfo(symbol)
    return jsonify(result = result, stockStats = stockStats)
    # return jsonify(result = 'success', stock = {'price': 131.96, 'change': '-5.13 (-3.74%)', 'symbol': 'AAPL'})




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
    share = int(request.form['share'])
    result = db.buyStock(username, symbol, share)
    balence = db.getBalence(username)
    return jsonify(result = result, balence = balence)
    # return jsonify(result = 'success', balence = 23.99)








@app.route('/refreshWatchList', methods = ['POST'])
def refreshWatchList():
    username = request.form['username']
    db.updateAllStockInfo()
    return jsonify(result = db.getWatchList(username))







@app.route('/portfolio/<username>')
def portfolio(username):
    return render_template('Portfolio.html')

# @app.route('/portfolio')
# def portfolioRedirect():
#     redirect('/portfolio'+current_user.username)



@app.route('/getOwnedStock', methods = ['POST']) 
def getOwnedStock():
    db.updateAllStockInfo()
    username = request.form['username']
    result = db.getOwnedStock(username=username)
    print('\n\n\n\n\n\n\n\n\n\n\n----------------------------------------------------------\n', username, result, '\n-----------------------------------------------\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    return jsonify(result = result)
    # return jsonify(result = { 'stocks': [{ 'symbol': 'AAPL', 'price': 131.96, 'share': 4, 'value': 527.84 }, { 'symbol': 'GOOG', 'price': 1835.74, 'share': 3, 'value': 5507.22 }, { 'symbol': 'GOOG', 'price': 1835.74, 'share': 3, 'value': 5507.22 }, { 'symbol': 'GOOG', 'price': 1835.74, 'share': 3, 'value': 5507.22 }], 'totalValue': 6035.06, 'balence': 213.99 })



@app.route('/sellStock', methods = ['POST'])
def sellStock():
    username = request.form['username']
    symbol = request.form['symbol']
    share = int(request.form['share'])
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\----------------------------------------------------------\n', username, symbol, share, '\n-----------------------------------------------\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    print(type(share))
    result = db.sellStock(username, symbol, share)
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n----------------------------------------------------------\n', 'result done', '\n-----------------------------------------------\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    balence = db.getBalence(username)
    stockInfo = db.getSingleStockOwned(username, symbol)
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\----------------------------------------------------------\n', result, balence, stockInfo, '\n-----------------------------------------------\n\n\n\n\n\n\n\n\n\n\n\n')

    return jsonify(result = result, balence = balence, stock = stockInfo)
    # return jsonify(result = 'success', balence = 213.44, stock = {'symbol': 'AAPL', 'price': 131.96, 'share': 3, 'value': 395.88})










@app.route('/balence', methods = ['POST'])
def balence():
    username = request.form['username']
    return jsonify(result = db.getBalence(username))