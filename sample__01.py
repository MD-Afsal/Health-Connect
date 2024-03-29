import mysql.connector
import qrcode
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


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/home_')
def home2():
    return render_template('home2.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['emailId']
        password = request.form['passwordId']
        mycursor.execute("SELECT * FROM tbl_login WHERE user=%s AND pass=%s", (username, password))
        user = mycursor.fetchone()
        if user:
            session['user'] = request.form.get('user')
            return redirect(url_for('home'))
        else:
            msg = "Incorrect user or password!"
            return render_template('login.html', msg=msg)
    return redirect(url_for('index'))


@app.route('/image/<int:image_id>')
def get_image(image_id):
    mycursor.execute("SELECT doc_img FROM tbl_doctor_details WHERE id = %s", (image_id,))
    image_data = mycursor.fetchone()[0]
    # mycursor.close()
    return Response(image_data, mimetype='image/jpeg')  # Adjust mimetype based on your image type


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

        sql = '''insert into tbl_doctor_details(doc_name, doc_img, doc_img_path, category, district, city, address, hospital_name, phone, 
                time_IN, time_OUT, map_code) values(%s ,%s ,%s, %s ,%s ,%s, %s ,%s, %s ,%s, %s, %s)'''

        val = (doc_name, image_data, image_path, category, district, city, address, hospital_name, phone, time_in, time_out, map_code)

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


@app.route('/get_doctor_details', methods=['GET'])
def get_doctor_details():

    category = request.args.get('category')

    query = "SELECT * FROM tbl_doctor_details WHERE category = %s"
    mycursor.execute(query, (category,))
    doctor_details = mycursor.fetchall()

    html_content = render_template('doctor_details.html', doctor_details=doctor_details)
    return html_content


def generate_qr_code(data, filename="my_qrcode.png"):
    """
    Generate a QR code from the provided data and save it as an image.

    Parameters:
        data (str): The data to be encoded in the QR code.
        filename (str): The filename to save the QR code image. Default is "my_qrcode.png".
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image
    img.save(filename)

    print("QR Code generated successfully!")


def get_data_to_encode():
    """
    Prompt the user to enter the data to encode in the QR code.

    Returns:
        str: The data entered by the user.
    """
    data = input("Enter the data to encode in the QR code: ")
    return data


# Example usage:
if __name__ == "__main__":
    #data_to_encode = get_data_to_encode()
    #generate_qr_code(data_to_encode)
    app.run(debug=True)

