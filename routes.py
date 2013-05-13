from flask import *
from functools import wraps
from flask.ext.mail import *
import sqlite3

app = Flask(__name__)
DATABASE = '/home/tanjinyi/projectpractice1/DATABASE.db' #database path
app.secret_key = "oh really?"
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE']) #connect to database

def login_required(test): #ensures pages that require login well, require login
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs) #test if logged_in exists
        else:
            flash('You need to login first.') #not true, redirecting+flash message
            return redirect(url_for('log'))
    return wrap

@app.route('/')
def home():
    g.db = connect_db()
    cur = g.db.execute('select * FROM merch ORDER BY pid')
    merch = [dict(pid=row[0], merchandise=row[1], price=row[2]) for row in cur.fetchall()]
    return render_template('welcome.html', merch = merch) #it's the welcome page!

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        checking = False
        userinsert = request.form['username'] # temp store variables
        passinsert = request.form['password']
        emailinsert = request.form['email']
        addressinsert = request.form['address']
        if checking == False:
            g.db = connect_db()
            checkuser = g.db.execute('SELECT * FROM users WHERE username="'+userinsert+'"')
            if not checkuser.fetchone():
                g.db.execute('INSERT INTO users VALUES(?, ?, ?, ?)', (userinsert, passinsert, emailinsert, addressinsert))
                g.db.commit()
                g.db.close()
                return redirect(url_for('log'))
            else:
                message = "User already exists."
    return render_template('register.html', message = message) #returns message flash if wrong, else redirects


@app.route('/logout')
def logout():
    session.pop('logged_in', None) #clear variables
    session.pop('user', None) #clear variables
    flash('You were logged out')
    return redirect(url_for('log'))

'''@app.route('/forgot', methods=['GET', 'POST']) #ain't done till it's done
def forgot_pass():
    g.db = connect_db()
    if request.method == 'POST':
        forgotuser = request.form['username']
        forgotemail = request.form['email']
        databaseselect = g.db.execute('SELECT * FROM users WHERE username="'+forgotuser+'"AND email="'+forgotemail+'"')
        if not databaseselect:
            message = "There is no current existing user with the username and email. Please try again or register."
        else:
            message = "Please check your email, your password has been sent to you!"
    # insert email conditions here
    return render_template('forgot.html', message = message)'''

@app.route('/log', methods=['GET', 'POST'])
def log():
    error = None
    if request.method == 'POST':
        g.db = connect_db()
        checkuser = g.db.execute("SELECT * FROM users WHERE username=? AND password=?", [request.form['username'], request.form['password']])
        validation = False
        for row in checkuser:
            if request.form['username'] == row[0] and request.form['password'] == row[1]: #validate user and password
                validation = True
        if validation == False:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            session['user'] = request.form['username']
            return redirect(url_for('store'))
    return render_template('log.html', error=error)

@app.route('/store', methods=['GET','POST'])
@login_required
def store():
    user = session['user']
    g.db  = connect_db()
    cur = g.db.execute('select * FROM merch ORDER BY pid')
    error = None
    merch = [dict(pid=row[0], merchandise=row[1], price=row[2]) for row in cur.fetchall()]
    totalprice = 0
    if request.method == 'POST':
        itemcart = False
        g.db = connect_db()
        g.db.execute('DELETE FROM currentorder WHERE username="'+user+'"')
        for pid in range (1,14):
            if str(request.form[str(pid)]).isdigit():
                quantitystore = int(request.form[str(pid)])
            elif request.form[str(pid)].isdigit() == False:
                error = 'Please input positive integers only.'
                break
            if quantitystore > 0:
                namestore = request.form['a'+str(pid)]
                originalstore = float(request.form['b'+str(pid)])
                totalprice += originalstore*quantitystore
                itemcart = True
                g.db.execute('INSERT INTO currentorder VALUES(?, ?, ?, ?)', [user, namestore, quantitystore, originalstore])
        session['totalprice'] = totalprice
        g.db.commit()
        if itemcart:
            return redirect(url_for('confirm'))
        elif error == None:
            error = 'You placed a blank order!'
    g.db.close()
    return render_template('store.html', merch=merch, error=error, user=user)

@app.route('/confirm', methods=['GET','POST'])
def confirm():
    g.db = connect_db()
    cur = g.db.execute('SELECT * from currentorder')
    currentorder = [dict(merchandise=row[1], quantity=row[2], price=row[2]*row[3]) for row in cur.fetchall()]
    totalprice = session['totalprice']
    g.db.close()
    '''if request.method == 'POST':
        return redirect(url_for('complete'))'''
    return render_template('confirm.html', currentorder = currentorder, totalprice = totalprice)

@app.route('/complete', methods=['GET','POST'])
def complete(): #MUST IMPLEMENT EMAIL BUT NO TIME
    return render_template('complete.html')