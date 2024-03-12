import mysql.connector
from flask import Flask, render_template, request, url_for, redirect, session, Response
from flask_session import Session

app = Flask(__name__)
app.secret_key = '1234'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Admin93@",
    database="HealthCon"
)
mycursor = mydb.cursor()


@app.route('/')
def index():
    if not session.get('name'):
        return render_template('login.html')
    return render_template('main.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        user = request.form['iduser']
        pasw = request.form['idpass']
        email = request.form['idemail']
        sql = "insert into tbl_login(username,password,email) values(%s,%s,%s)"
        val = (user, pasw, email)
        mycursor.execute(sql, val)
        mydb.commit()
        session['user'] = request.form.get('iduser')
        session['password'] = request.form.get('idpass')
        session['email'] = request.form.get('idemail')
        mycursor.execute("select id from tbl_login where username=%s and password=%s",(session.get('user'),session.get('password')))
        user_id = mycursor.fetchone()
        session['id'] = user_id
        return redirect(url_for('home'))
    return redirect(url_for('index'))


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['emailId']
        password = request.form['passwordId']
        mycursor.execute("SELECT * FROM tbl_login WHERE username=%s AND password=%s", (username, password))
        user = mycursor.fetchall()
        if user:
            user1 = user[0]
            session['id'] = user1[0]
            session['user'] = user1[1]
            session['email'] = user1[2]
            session['password'] = user1[3]
            # user refers the list with in a tuple and the user1 refers the 1st tuple on the list
            return redirect(url_for('home'))
        else:
            msg = "Incorrect user or password!"
            return render_template('login.html', msg=msg)
    return redirect(url_for('index'))


# image retrival using id
@app.route('/image/<int:image_id>')
def get_image(image_id):
    mycursor.execute("SELECT doc_img FROM tbl_doctor_details WHERE id = %s", (image_id,))
    image_data = mycursor.fetchone()[0]
    # mycursor.close()
    return Response(image_data, mimetype='image/jpeg')  # Adjust mimetype based on your image type


@app.route('/home')
def home():
    return render_template('main.html')


@app.route('/home_')
def home2():
    return render_template('home2.html')


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

        sql = '''insert into tbl_doctor_details(doc_name, doc_img, doc_img_path, category, district, city, address, hospital_name, phone, 
        time_IN, time_OUT) values(%s ,%s ,%s, %s ,%s ,%s, %s ,%s, %s ,%s, %s)'''

        val = (doc_name, category, district, city, address, hospital_name, phone, time_in, time_out)

        mycursor.execute(sql, val)
        mydb.commit()
    return render_template('adminPage.html')
    

if __name__ == '__main__':
    app.run(debug=True)
