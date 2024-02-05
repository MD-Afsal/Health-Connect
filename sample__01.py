import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Admin93@",
  database="Demo_test"
)
print("---------------")

mycursor = mydb.cursor()

sql = "INSERT INTO sample2 (sam1 , sam2) VALUES (%s, %s)"
val = ("iamnot","iamafsal")
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")