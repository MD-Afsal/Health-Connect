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
        session['user'] = request.form.get('user')
        return redirect(url_for('home'))
    return redirect(url_for('index'))


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['emailId']
        password = request.form['passwordId']
        mycursor.execute("SELECT * FROM tbl_login WHERE username=%s AND password=%s", (username, password))
        user = mycursor.fetchone()
        if user:
            session['user'] = request.form.get('user')
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
    return render_template('home.html')


@app.route('/home_')
def home2():
    return render_template('home2.html')


@app.route('/head')
def head():
    return render_template('head.html')


@app.route('/chest')
def chest():
    return render_template('chest.html')


@app.route('/hand')
def hand():
    return render_template('hand.html')


@app.route('/stomach')
def stomach():
    return render_template('stomach.html')


@app.route('/leg')
def leg():
    return render_template('leg.html')


@app.route('/posterior')
def posterior():
    return render_template('posterior.html')


@app.route('/insert_doctor_rec', methods=['POST', 'GET'])
def insert_rec():
    if request.method == 'POST':
        doc_name = request.form['doc_name']
        image = request.files['doc_img']
        image_data = image.read()
        image_path = f"uploads/{image.filename}"
        category = request.form['doc_cat']
        district = request.form['doc_dict']
        city = request.form['doc_city']
        address = request.form['doc_addr']
        hospital_name = request.form['doc_hos']
        phone = request.form['doc_num']
        time_in = request.form['doc_time_in']
        time_out = request.form['doc_time_out']
        map_code = request.form['map_code']

        sql = '''insert into tbl_doctor_details(doc_name, doc_img, doc_img_path, category, district, city, address,
         hospital_name, phone, time_IN, time_OUT, map_code) values(%s ,%s ,%s, %s ,%s ,%s, %s ,%s, %s ,%s, %s, %s)'''

        val = (doc_name, image_data, image_path, category, district, city, address, hospital_name, phone, time_in, time_out, map_code)

        mycursor.execute(sql, val)
        mydb.commit()
    return render_template('adminPage.html')


# for user input action (admin page)
@app.route('/insert_user_rec', methods=['POST', 'GET'])
def insert_user_rec():
    global msg
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_pass = request.form['user_pass']
        mycursor.execute("SELECT * FROM tbl_login WHERE username=%s AND password=%s", (user_name, user_pass))
        user = mycursor.fetchone()
        if user:
            return render_template('userAccountModificationPage.html')
            # create function for user modification in user profile
        else:
            msg = "Incorrect user or password!"
    return render_template('adminPage.html', msg=msg)


@app.route('/get_doctor_details', methods=['GET'])
def get_doctor_details():

    category = request.args.get('category')

    query = "SELECT * FROM tbl_doctor_details WHERE category = %s"
    mycursor.execute(query, (category,))
    doctor_details = mycursor.fetchall()

    html_content = render_template('doctor_details.html', doctor_details=doctor_details)
    return html_content



if __name__ == '__main__':
    app.run(debug=True)
