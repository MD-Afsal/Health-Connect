import mysql.connector
from flask import Flask, render_template, request, url_for, redirect, session, Response
from flask_session import Session
import base64
import qrcode

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
# global user_id
global msg


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
        mycursor.execute("select id from tbl_login where username=%s and password=%s",
                         (session.get('user'), session.get('password')))
        user_id = mycursor.fetchone()
        session['id'] = user_id
        return redirect(url_for('get_userinput'))
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


# getting the user details
@app.route('/user_details', methods=['GET', 'POST'])
def get_userinput():
    if request.method == 'POST':
        user_name = request.form['user_name']
        image = request.files['user_img']
        user_image = image.read()
        user_age = request.form['user_age']
        user_gender = request.form['user_gender']
        user_bloodgrp = request.form['user_bloodgrp']
        affected_with = request.form['user_affected_with']
        sql = '''update tbl_user_details set name=%s, user_img=%s, age=%s, gender=%s,
         blood_group=%s, affected_with=%s where id=%s'''
        user_id_tup = session['id']
        user_id = user_id_tup[0]
        print(user_id)
        val = (user_name, user_image, user_age, user_gender, user_bloodgrp, affected_with, user_id)

        mycursor.execute(sql, val)

        mydb.commit()
        return redirect(url_for('home'))
    return render_template('user_details.html')


# image retrival using id
@app.route('/image/<int:image_id>')
def get_image1(image_id):
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

        val = (doc_name, image_data, image_path, category, district, city, address, hospital_name, phone, time_in,
               time_out, map_code)

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


@app.route('/get_card_details', methods=['GET'])
def get_card_details():
    phone_no = request.args.get('phone_no')
    print("Received phone number:", phone_no)
    query = "select * from tbl_doctor_details where phone = %s"
    mycursor.execute(query, (phone_no,))
    doc_details = mycursor.fetchall()
    para = render_template('card_details.html', doc_details=doc_details)
    return para


@app.route('/qr_image')
def get_image():
    user_Id = session['id']
    print("User id :", user_Id)
    type_id = type(user_Id)
    if type_id == int:
        temp_list = []
        temp_list.append(user_Id)
        user_Id = tuple(temp_list)
    elif type_id == tuple:
        pass
    mycursor.execute("SELECT rep1,rep2,rep3,rep4,rep5,rep6,rep7,rep8 FROM tbl_user_medicalreport_images WHERE id = %s",
                     (user_Id))
    blob_data_list = []

    for row in mycursor.fetchall():
        # print(row)
        for i in range(0, 7):
            if row[i] is not None:
                base64_blob_data = base64.b64encode(row[i]).decode('utf-8')
                blob_data_list.append(base64_blob_data)

    # getcontentimage()

    return render_template('qrshare.html', blob_data_list=blob_data_list)


@app.route('/uploads', methods=['POST', 'GET'])
def uploads():
    if request.method == 'POST':
        image1 = request.files['rep1']
        image_data1 = image1.read()
        image2 = request.files['rep2']
        image_data2 = image2.read()
        image3 = request.files['rep3']
        image_data3 = image3.read()
        image4 = request.files['rep4']
        image_data4 = image4.read()
        image5 = request.files['rep5']
        image_data5 = image5.read()
        image6 = request.files['rep6']
        image_data6 = image6.read()
        image7 = request.files['rep7']
        image_data7 = image7.read()
        image8 = request.files['rep8']
        image_data8 = image8.read()
        sql = '''update tbl_user_medicalreport_images set rep1=%s, rep2=%s, rep3=%s, rep4=%s, rep5=%s, rep6=%s, rep7=%s,
        rep8=%s where id=%s'''
        user_id = session['id']

        print("User_id", user_id)
        val = (image_data1, image_data2, image_data3, image_data4, image_data5, image_data6, image_data7,
               image_data8, user_id)
        mycursor.execute(sql, val)
        mydb.commit()
        # creating qr for uploaded images
        # fun_img_qr_get()
    return render_template('uploads.html')


# Function to generate QR code for multiple image Blobs and store in MySQL
def generate_and_store_multi_image_qr(image_blobs):
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    user_Id = session['id']
    # Add image Blobs data to QR code
    for blob_data in image_blobs:
        qr.add_data(blob_data)

    qr.make(fit=True)

    # Generate QR code image
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert image to byte stream
    img_byte_array = img.getvalue()

    # Update existing record in MySQL with the new QR code image
    mycursor.execute("UPDATE tbl_user_details SET qr_code = %s WHERE id = %s", (img_byte_array, user_Id))
    print("Created qr successfully")
    # Commit the transaction
    mydb.commit()


@app.route('/qr_code_')
def fun_img_qr_get():
    user_Id = session['id']
    type_id = type(user_Id)
    if type_id == int:
        temp_list = [user_Id]
        user_Id = tuple(temp_list)
    elif type_id == tuple:
        pass
    mycursor.execute("SELECT rep1,rep2,rep3,rep4,rep5,rep6,rep7,rep8 FROM tbl_user_medicalreport_images WHERE id = %s",
                     (user_Id))

    image_blobs1 = []
    for row in mycursor.fetchall():
        # print(row)
        for i in range(0, 7):
            if row[i] is not None:
                base64_blob_data = base64.b64encode(row[i]).decode('utf-8')
                image_blobs1.append(base64_blob_data)
    # Convert Blob image data from base64 to bytes
    print(image_blobs1)

    # Update Blob data decoding with error handling
    image_blobs = []
    for blob in image_blobs1:
        try:
            base64_blob_data = base64.b64decode(blob.split(',')[0])
            image_blobs.append(base64_blob_data)
        except IndexError:
            print("Error: Unable to split blob data. Skipping...")

    generate_and_store_multi_image_qr(image_blobs)


"""
# Function to generate QR code for multiple image Blobs
def generate_multi_image_qr(image_blobs, qr_code_path):
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add image Blobs data to QR code
    for blob_data in image_blobs:
        qr.add_data(blob_data)

    qr.make(fit=True)

    # Generate QR code image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code image to file
    img.save(qr_code_path)
    print("Generated successfully")
    return render_template('qrshare.html')


def getcontentimage():
    print("HElloooo")
    user_Id = session['id']
    print(user_Id)
    image_blobs = []
    mycursor.execute("SELECT rep1,rep2 FROM tbl_user_medicalreport_images WHERE id = %s",
                     (user_Id,))
    for row in mycursor.fetchall():
        image_blobs.append(row)
    # print("Image blob data : --->>>>",image_blobs)
    # Convert Blob image data from base64 to bytes
    image_blobs = [base64.b64decode(blob.split(',')[1]) for blob in image_blobs]
    qr_code_path = "multi_image_qr.png"  # Name of the output QR code file
    generate_multi_image_qr(image_blobs, qr_code_path)
"""

if __name__ == '__main__':
    '''image_blobs = [
        # Base64 encoded image data as Blob
        "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAAAAAAAD/4Q...",
        "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAAAAAAAD/4R..."
        # Add more Blob image data as needed
    ]

    # Convert Blob image data from base64 to bytes
    image_blobs = [base64.b64decode(blob.split(',')[1]) for blob in image_blobs]

    qr_code_path = "multi_image_qr.png"'''
    app.run(debug=True)
