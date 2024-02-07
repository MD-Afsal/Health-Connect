from flask import Flask, redirect, url_for, render_template, request
import mysql.connector


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


@app.route('/signup',methods=['POST' ,'GET'])
def signup():
    if request.method == 'POST':
        user = request.form['iduser']
        pasw = request.form['idpass']
        email = request.form['idemail']
        sql = "insert into login(user,pass,email) values(%s,%s,%s)"
        val = (user,pasw,email)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('home'))
    return redirect(url_for('index'))

@app.route('/home')
def home():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)
