import mysql.connector
from flask import Flask, render_template, request, url_for, redirect,session

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Admin93@",
    database="HealthCon"
)
mycursor = mydb.cursor()


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    session['text'] = ""
    session['trans'] = ""
    session['lang'] = ""
    msg = ''
    if request.method == 'POST' and 'txt_user' in request.form and 'txt_pass' in request.form:
        username = request.form['txt_user']
        password = request.form['txt_pass']
        cursor = mysql.connection.cursor(mydb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_signup WHERE username = % s AND password = % s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['email'] = account['email']
            session['password'] = account['password']
            return render_template('home.html', user=session.get('username'), email=session['email'],
                                   pasw=session['password'])
        else:
            msg = 'Incorrect username / password !'
    return render_template('signin.html', msg=msg)


@app.route('/insert_rec', methods=['POST', 'GET'])
def insert_rec():
    if request.method == 'POST':
        doc_name = request.form['doc_name']
        category = request.form['doc_cat']
        district = request.form['doc_dict']
        city = request.form['doc_city']
        address = request.form['doc_addr']
        hospital_name = request.form['doc_hos']
        phone = request.form['doc_num']
        time_in = request.form['doc_time_in']
        time_out = request.form['doc_time_out']

        sql = '''insert into tbl_docter(doc_name, category, district, city, address, hospital_name, phone, 
                time_IN, time_OUT) values(%s ,%s ,%s, %s ,%s ,%s, %s ,%s ,%s)'''

        val = (doc_name, category, district, city, address, hospital_name, phone, time_in, time_out)

        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('adminPage.html')


if __name__ == '__main__':
    app.run(debug=True)
