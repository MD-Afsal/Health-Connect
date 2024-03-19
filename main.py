from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Samsung753',
    'database': 'HealthCon'
} 


@app.route('/')
def main():
    return render_template('chest.html')


@app.route('/get_doctor_details', methods=['GET'])
def get_doctor_details():

    category = request.args.get('category')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = "SELECT * FROM tbl_doctor_details WHERE category = %s"
    cursor.execute(query, (category,))
    doctor_details = cursor.fetchall()

    conn.close()

    html_content = render_template('doctor_details.html', doctor_details=doctor_details)
    return html_content



if "__main__" == __name__:
    app.run(debug=True, port='32')