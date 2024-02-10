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


@app.route('/backpose')
def rotateimg():
    return render_template('rotateimg.html')


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
