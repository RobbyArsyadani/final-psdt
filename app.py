from flask import (
    Flask, redirect, render_template, request,flash, session, url_for, jsonify
)
from db import db_connection

app = Flask(__name__)
app.secret_key = 'Secretkey'

@app.route('/')
def index():
    conn = db_connection()
    cur = conn.cursor()
    sql = """SELECT bor.id, usr.name FROM users usr JOIN borrowed bor ON bor.user_id = usr.id"""
    cur.execute(sql)
    borrowed = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', borrowed=borrowed)



@app.route('/create', methods = ['GET','POST'])
def create():
     if request.method == 'POST':
      book_title = request.form ['book_title']
      date_borrowed = request.form ['pinjam']
      date_due = request.form ['pengembalian']
      days_of_loan = request.form['total hari']
      user_id = session.get('user_id')

      db = db_connection()
      cur = db.cursor()
      sql = ("""INSERT INTO borrowed (book_title,date_borrowed,date_due,days_of_loan,user_id) VALUES ('%s','%s','%s','%s','%s')""" %
      (book_title,date_borrowed,date_due,days_of_loan,user_id))
      cur.execute(sql)
      db.commit()
      cur.close()
      db.close()
    
     return render_template('create.html')

@app.route('/register', methods = ['GET','POST'])
#function for registration
def register():
    if request.method == 'POST':
     name = request.form ['name']   
     address = request.form['address']
     phone = request.form['phonenum']
     password = request.form['password']
     conn = db_connection() #connecting to the database
     cur = conn.cursor() 
     register = (""" INSERT INTO users (name,address,phone,password) VALUES ('%s','%s','%s','%s')""" % (name,address,phone,password))
     cur.execute("SELECT * FROM users WHERE name = %(name)s", {'name':name})
     check = cur.fetchone()
     error = ""
     #checking if username already exists
     if check :
       error = "This username already exists, please enter a new one"
     else:
         cur.execute(register)
     flash(error)
     conn.commit()
     cur.close()
     conn.close()

    return render_template ('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ function to show and process login page """
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']

        conn = db_connection()
        cur = conn.cursor()
        sql = """
            SELECT id, name
            FROM users
            WHERE name = '%s' AND password = '%s'
        """ % (username, password)
        cur.execute(sql)
        user = cur.fetchone()

        error = ''
        if user is None:
            error = 'Wrong credentials. No user found'
        else:
            session.clear()
            session['user_id'] = user[0]
            session['name'] = user[1]
            return redirect(url_for('index'))

        flash(error)
        cur.close()
        conn.close()

    return render_template('login.html')

@app.route('/detail/<int:borrowed_id>', methods=['GET'])
def read(borrowed_id):
    # find the borrowed with id = borrowed_id, return not found page if error
    conn = db_connection()
    cur = conn.cursor()
    sql = """
        SELECT bor.id, bor.book_title, bor.date_borrowed, bor.date_due, bor.days_of_loan FROM borrowed bor JOIN users usr ON usr.id = bor.user_id WHERE bor.id = %s
    """ % borrowed_id
    cur.execute(sql)
    borrowed = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('detail.html', borrowed=borrowed)

@app.route('/list', methods =['GET','POST'])
def booklist():
    """ function to show list of all books """
    db = db_connection()
    cur = db.cursor()
    sql = """SELECT * FROM books"""
    cur.execute(sql)
    rv = cur.fetchall()
    return render_template('list.html', rv=rv)
    
@app.route('/edit/<int:borrowed_id>', methods=['GET', 'POST'])
def edit(borrowed_id):
    if not session :
        return redirect(url_for('login'))
    if request.method == 'POST':
        conn = db_connection()
        cur = conn.cursor()
        book_title = request.form['book_title']
        date_borrowed= request.form['pinjam']
        date_due = request.form['pengembalian']
        days_of_loan = request.form['total hari']

        sql_params = (book_title, date_borrowed, date_due, days_of_loan, borrowed_id)

        sql = "UPDATE borrowed SET book_title = '%s', date_borrowed = '%s', date_due = '%s', days_of_loan = '%s' WHERE id = %s" % sql_params
        print(sql)
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()
        # use redirect to go to certain url. url_for function accepts the
        # function name of the URL which is function index() in this case
        return redirect(url_for('index'))

    # find the record first
    conn = db_connection()
    cur = conn.cursor()
    sql = 'SELECT bor.id, bor.book_title, bor.date_borrowed, bor. date_due, bor. days_of_loan FROM borrowed bor WHERE id = %s' % borrowed_id
    cur.execute(sql)
    borrowed = cur.fetchone()
    cur.close()
    conn.close()

    return render_template('edit.html', borrowed=borrowed)

@app.route('/delete/<int:borrowed_id>', methods=['GET','POST'])
def delete(borrowed_id):
    if not session:
        return redirect(url_for('login'))

    conn = db_connection()
    cur = conn.cursor()
    sql = 'DELETE FROM borrowed WHERE id = %s' % borrowed_id
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()
    return jsonify({'status': 200, 'redirect': '/'})

