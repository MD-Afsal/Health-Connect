from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('user_details.html')

if "__main__" == __name__:
    app.run(debug=True)