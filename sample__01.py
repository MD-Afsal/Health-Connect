import mysql.connector
from flask import Flask, render_template, request, url_for, redirect, session

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="HealthCon"
)
mycursor = mydb.cursor()


@app.route('/')
def index():
    return redirect(url_for('insert_rec'))


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
        image = request.files['doc_img']
        image_data = image.read()
        image_path = f"uploads/{image.filename}"

        '''if 'doc_img' in request.files:
            image = request.files['doc_img']
            image_path = f"uploads/{image.filename}"
            image.save(image_path)'''

        category = request.form['doc_cat']
        district = request.form['doc_dict']
        city = request.form['doc_city']
        address = request.form['doc_addr']
        hospital_name = request.form['doc_hos']
        phone = request.form['doc_num']
        time_in = request.form['doc_time_in']
        time_out = request.form['doc_time_out']

            #insert_query = 'INSERT INTO images (image_path) VALUES (%s)'
            #mycursor.execute(insert_query, (image_path1,))
            #mydb.commit()

            #return 'Image uploaded successfully!'

        sql = '''insert into tbl_docter(doc_name, doc_img, doc_img_path, category, district, city, address, hospital_name, phone, 
                time_IN, time_OUT) values(%s ,%s ,%s, %s ,%s ,%s, %s ,%s, %s ,%s, %s)'''

        val = (doc_name, image_data, image_path, category, district, city, address, hospital_name, phone, time_in, time_out)

        mycursor.execute(sql, val)
        mydb.commit()
    return render_template('adminPage.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' in request.files:
        image = request.files['image']
        image_path = f"uploads/{image.filename}"
        image.save(image_path)

        insert_query = 'INSERT INTO images (image_path) VALUES (%s)'
        mycursor.execute(insert_query, (image_path,))
        mydb.commit()

        return 'Image uploaded successfully!'
    return 'Image upload failed.'


if __name__ == '__main__':
    app.run(debug=True)
