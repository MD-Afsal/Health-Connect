import mysql.connector
from flask import Flask, render_template, request, url_for, redirect, session, Response

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
    return render_template('adminPage.html')


@app.route('/head')
def head():
    return render_template('head.html')


@app.route('/backpose')
def rotateimg():
    return render_template('rotateimg.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['emailId']
        password = request.form['passwordId']
        mycursor.execute("SELECT * FROM login WHERE user=%s AND pass=%s", (username, password))
        user = mycursor.fetchone()
        if user:
            session['user'] = request.form.get('user')
            return redirect(url_for('home'))
        else:
            msg = "Incorrect user or password!"
            return render_template('login.html', msg=msg)
    return redirect(url_for('index'))



@app.route('/insert_doctor_rec', methods=['POST', 'GET'])
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


# for user input action (admin page)
@app.route('/insert_user_rec', methods=['POST', 'GET'])
def insert_user_rec():
    global msg
    if request.method == 'POST':
        # on process and we need to convert the code to user input
        user_name = request.form['user_name']
        user_pass = request.form['user_pass']
        mycursor.execute("SELECT * FROM tbl_login WHERE username=%s AND password=%s", (user_name, user_pass))
        user = mycursor.fetchone()
        if user:
            return render_template('userAccountModificationPage.html')    # create function for user modification in user profile
        else:
            msg = "Incorrect user or password!"
    return render_template('adminPage.html', msg=msg)

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
