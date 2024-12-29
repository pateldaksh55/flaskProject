from flask import Flask, render_template, request, redirect,session,url_for
from flask_session import Session
import re
import mysql.connector

app = Flask(__name__)
app.secret_key='abcd'
db_config = {

    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'daksh'
}


def get_connection():
    return mysql.connector.connect(**db_config)


def create_USER_table():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS data(
    
    email VARCHAR(255) NOT NULL PRIMARY KEY ,
    password VARCHAR(255) NOT NULL)
    """)
    con.commit()
    cur.close()
    con.close()

create_USER_table()
@app.route('/',methods=['GET'])
def index():
    return render_template('signup.html')


@app.route('/', methods=['POST'])
def submit():
    mesage=''
    if request.method == 'POST'and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmpassword']
        con = get_connection()
        cur = con.cursor()
        cur.execute("select * from data where email=%s", (email,))
        acc = cur.fetchone()
        if acc:
            mesage = 'Already Exist! '
        elif password != confirm_password:
            mesage = 'Password Does Not Match!'
        else:
            try:

                cur.execute("INSERT INTO data (email, password) VALUES (%s, %s)", (email, password))
                con.commit()
                cur.close()
                con.close()
                return redirect(url_for('login'))
            except Exception as e:
                print("Error inserting values:", e)
                return 'Error inserting values'
        return render_template('signup.html', mesage=mesage)

@app.route('/login')
def login():
    return render_template('index.html')

@app.route('/new',methods=['GET','POST'])
def login1():
    mesage=''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password =request.form['password']
        con = get_connection()
        cur = con.cursor()
        cur.execute("select * from data where email=%s and password=%s", (email, password))
        user=cur.fetchone()
        if user:
            session['logged_in'] = True
            session['email'] = user[0]
            session['password'] =user[1]
            mesage='logged in successfully'
            return redirect(url_for('home'))
        else:
            mesage='Invalid email or password'
            return render_template('index.html', mesage=mesage)
    return render_template('index.html')


@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/home')
def home():
    return render_template('new.html')

@app.route('/ahemdabad')
def ahemdabad():
    return render_template('ahemdabad.html')

@app.route('/kutch')
def kutch():
    return render_template('kutch.html')

@app.route('/gir')
def gir():
    return render_template('gir.html')







if __name__== '_main_':
    app.run()