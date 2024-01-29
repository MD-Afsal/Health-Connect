from flask import Flask, render_template
from flask_mysaldb import MySQL

app = Flask(__name__)

@app.config['MYSQL_HOST'] = 'localhost'

@app.route('/')
def home():
    return render_template('head.html')


@app.route('/Rotated_image')
def rotated_image():
    return render_template('Rotated_image.html')

if __name__ == '__main__':
    app.run(debug=True)
