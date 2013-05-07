from flask import *
from functools import wraps
import sqlite3

DATABASE = '/home/tanjinyi/projectpractice1/merchandise.db'
orderdatabase = '/home/tanjinyi/projectpractice1/orders.db'
userdatabase = '/home/tanjinyi/projectpractice1/userdatabase.db'

app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = "oh really?"

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def submit_order():
    return sqlite3.connect(app.config['orderdatabase'])

def user_table():
    return sqlite3.connect(app.config['userdatabase'])

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('log'))
    return wrap

@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        message = None
        userinsert = request.form['username'] # temp store variables
        passinsert = request.form['password']
        verifypass = request.form['verifypass']
        if verifypass != passinsert:
            message = "Your passwords did not match. Try again."
        elif userinsert == "" or passinsert == "" or emailinsert == "" or addressinsert == "":
            message = "You did not enter in one of the fields. Please fill in all fields."
        if not message:
            emailinsert = request.form['email']
            addressinsert = request.form['address']
            users.db = user_table()
            users.db.execute = ('CREATE TABLE IF NOT EXISTS user(username TEXT, password TEXT, email TEXT')
            users.db.execute = ('INSERT INTO TABLE users(?, ?, ?, ?)', userinsert, passinsert, emailinsert, addressinsert)
            return redirect(url_for('log'))
        else:
            return render_template('register.html', message = message)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('log'))

@app.route('/log', methods=['GET', 'POST'])
def log():
    #users.db = user_table()
    #checkuser = users.db.query("SELECT * FROM users WHERE username=? AND password=?", request.form['username'], request.form['password']) failing
    checkuser = True
    error = None
    if request.method == 'POST':
        if not checkuser:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            user = request.form['username']
            return redirect(url_for('store'))
    return render_template('log.html', error=error)

@app.route('/store', methods=['GET','POST'])
@login_required
def store():
    g.db  = connect_db()
    cur = g.db.execute('select pid, merchandise, price from merch')
    merch = [dict(pid=row[0], merchandise=row[1], price=row[2]) for row in cur.fetchall()]
    if request.method == 'POST':
        g.db.execute('create ?(merchandise TEXT, quantity TEXT, price TEXT) if not exists', user)
        for item in merch:         
            g.db.execute('insert into ? values (?, ?, ?)', user, merchandise, price
    g.db.close()
    return render_template('store.html', merch=merch)

@app.route('/submit', methods=['GET','POST'])
def submit():
    if request.method == 'POST':
        pidstore = []
        namestore = []
        quantitystore = []
        itemcart = False
        for pid in range (1,14):
            if request.form[pid] != 0:
                pidstore.append(pid)
                quantitystore.append(request.form[pid])
                namestore.append(request.form[a+str[pid]])
                itemcart = True
        if itemcart:
            order.db = submit_order()
            order.db.execute('DROP TABLE IF EXISTS ?', user)
            order.db.execute('CREATE TABLE ?(merchandise TEXT, quantity INT, price REAL', user)
            order.db.executemany('INSERT INTO ? VALUES(?, ?, ?)', user, pid, quantity, order_date)
            success = 'You have successfully placed an order.'
            return redirect(url_for('home'))
        else:
            error = 'You placed a blank order!'
            return render_template('store.html', error = error)

