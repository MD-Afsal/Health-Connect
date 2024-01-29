from flask import Flask, render_template
from flask_mysaldb import MySQL

app = Flask(__name__)

@app.config['MYSQL_HOST'] = 'localhost'

@app.route('/')
def login():
    return render_template('Home_page.html')


# first we need to redirect to the data upload page
# but here we are navigating to the main page
@app.route('/home')
def home():
    return render_template('Home_page.html')


@app.route('/Rotated_image')
def rotated_image():
    return render_template('Rotated_image.html')


if __name__ == '__main__':
    app.run(debug=True)
