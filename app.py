from click import password_option
from flask import Flask, render_template, redirect, request, session, url_for
import pyodbc

app = Flask(__name__)

# SQL Server bağlantı bilgilerini buraya girin
server = 'ArchCunq'
database = 'CampusChat_Test'
username = 'sa'
password = 'Base3003'

# Bağlantı dizesini oluşturun
conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=Yes'

def get_db_connection():
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to SQL Server: {e}")
        return None

@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/giris', methods=['GET','POST'])
def giris():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return "Eksik alanlar", 400

        conn = get_db_connection()
        if conn is None:
            return "Veritabanı bağlantı hatası", 500

        try:
            cursor = conn.cursor()
            cursor.execute('SELECT PASSWORD_ FROM users WHERE EMAIL = ?', (email,))
            result = cursor.fetchone()

            if result and result[0] == password:
                return redirect(url_for('index'))
            else:
                return "Kullanıcı adı veya şifre hatalı!", 401

        except pyodbc.Error as e:
            print(f"Veri sorgulama hatası: {e}")
            return "Veri sorgulama hatası", 500
        finally:
            conn.close()
    return render_template('giris.html')

@app.route('/kayit', methods=['GET', 'POST'])
def kayit():
    if request.method == 'POST':
        # Form verilerini al
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password = request.form.get('password')

        if not name or not surname or not email or not password:
            return "Missing fields", 400

        conn = get_db_connection()
        if conn is None:
            return "Database connection error", 500
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (NAME_, SURNAME, EMAIL, PASSWORD_) 
                VALUES (?, ?, ?, ?)
            ''', (name, surname, email, password))
            conn.commit()
            conn.close()
            return redirect(url_for('success'))
        except pyodbc.Error as e:
            print(f"Error inserting data: {e}")
            return "Error inserting data", 500

    # GET isteği için formu render et
    return render_template('kayit.html')

@app.route ('/success')
def success():
    return "Kayit Basarili!"

@app.route('/okullar')
def okullar():
    cursor.conn.execute('SELECT * FROM universities')
    universities = cursor.fetchall()
    return render_template('okullar.html')

if __name__ == "__main__":
    app.run(debug=True)