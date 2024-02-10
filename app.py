import mysql.connector
from flask import Flask, render_template, request, url_for, redirect

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


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        user = request.form['iduser']
        pasw = request.form['idpass']
        email = request.form['idemail']
        sql = "insert into login(user,pass,email) values(%s,%s,%s)"
        val = (user, pasw, email)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('home'))
    return redirect(url_for('index'))


@app.route('/home')
def home():
    return render_template('main.html')


@app.route('/backpose')
def rotateimg():
    return render_template('rotateimg.html')


if __name__ == '__main__':
    app.run(debug=True)
