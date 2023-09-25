from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def create_user_table():
    conn = sqlite3.connect('basic.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
            )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('temp.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')
        
        conn = sqlite3.connect('basic.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return render_template('signup.html', error='Username already exists')
        
        cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    else:
        return render_template('signup.html')
        
if __name__ == '__main__':
    create_user_table()
    app.run(debug=True)