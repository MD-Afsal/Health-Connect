from flask import Flask, render_template
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Admin93@",
  database="Demo_test"
)

app = Flask(__name__)


@app.route('/')
def login():
    return render_template('adminPage.html')


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
