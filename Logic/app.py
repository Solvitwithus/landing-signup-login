from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)
load_dotenv(dotenv_path=".env")
# mysql_password = os.getenv("MySQLPassword")
# print("MySQL Password:", mysql_password)

# # Add this line to print out the password for debugging
# print("Retrieved MySQL Password:", mysql_password)
@app.route("/Signup", methods=["POST"])
def Signup():
    db = None
    cursor = None

    if request.method == "POST":
        try:
            data = request.get_json()
            print("Received data:", data)

            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password=os.getenv("MySQLPassword"),
                database="landing"
            )

            cursor = db.cursor()

            sql = "INSERT INTO signup (username, email, password) VALUES (%s, %s, %s)"

            val = (username, email, password)
            cursor.execute(sql, val)
            db.commit()

            return jsonify({"message": "User created successfully"}), 201

            print("Connected to the database successfully!")
        except mysql.connector.Error as err:
            print(f"Database connection failed: {err}")
            return jsonify({"error": "Database connection failed"}), 500


        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

if __name__ == '__main__':
    app.run(debug=True)