from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('head.html')


@app.route('/Rotated_image')
def rotated_image():
    return render_template('Rotated_image.html')

if __name__ == '__main__':
    app.run(debug=True)
