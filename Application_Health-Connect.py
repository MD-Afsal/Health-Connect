from flask import Flask, render_template,request,url_for,redirect,session,send_file,Response
import mysql.connector,re

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="HealthCon"
)
@app.route('/')
@app.route('/login.html', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = request.form['iduser']
        p0asw = request.form['idpass']
        email = request.form['idemail']
        cursor = mydb.connection.cursor(mydb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_signup WHERE username = % s', (user,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif len(user) < 4:
            msg = 'User name must be greater than 3.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', user):
            msg = 'Username must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO tbl_signup VALUES (NULL, % s, % s, % s)', (user, email, pasw))
            mydb.connection.commit()
            return render_template('index.html')

    return render_template('login.html')

@app.route('/signin')
def signin():
    return render_template('login.html')
# first we need to redirect to the data upload page
# but here we are navigating to the main page
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/Rotated_image')
def rotated_image():
    return render_template('Rotated_image.html')


if __name__ == '__main__':
    app.run(debug=True)
