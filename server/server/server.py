from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import sqlite3
import shutil
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import  OUTPUT_MESH_PATH,generate_3d_model


DB_PATH = r"C:\Users\OWNER\Desktop\programming\convert 3D\convert3D\server\users.db"
UPLOAD_FOLDER = r"C:\Users\OWNER\Desktop\programming\convert 3D\convert3D\dl\images"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

app = Flask(__name__)
CORS(app)
os.makedirs(os.path.dirname(OUTPUT_MESH_PATH), exist_ok=True)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        conn.close()
        return jsonify({"message": "Registration successful"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "Username already exists"}), 400



@app.route('/login', methods=['POST'])
def login():
    data = request.json  
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Incorrect username or password."}), 400

uploaded_images = [] 

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"} 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_images():
    if 'image0' not in request.files: 
        return jsonify({"message": "לא נמצאו קבצים"}), 400
    for f in os.listdir(UPLOAD_FOLDER):
            os.remove(os.path.join(UPLOAD_FOLDER, f))

    images = request.files
    uploaded_images.clear()

    for key in images:  
        file = images[key]
        if file.filename == "":
            continue 
        if not allowed_file(file.filename):
            return jsonify({"message": f"קובץ {file.filename} אינו תמונה חוקית"}), 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        uploaded_images.append(file_path)
    try:
        generate_3d_model(UPLOAD_FOLDER, OUTPUT_MESH_PATH)
        return send_file(OUTPUT_MESH_PATH, as_attachment=True)
    except Exception as e:
        return jsonify({"message": f"שגיאה בבניית המודל: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

