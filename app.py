from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('sessions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject TEXT NOT NULL,
                    duration INTEGER,
                    notes TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('sessions.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sessions ORDER BY id DESC")
    sessions = c.fetchall()
    conn.close()
    return render_template('index.html', sessions=sessions)

@app.route('/add', methods=['POST'])
def add():
    subject = request.form['subject']
    duration = request.form['duration']
    notes = request.form['notes']
    if subject and duration:
        conn = sqlite3.connect('sessions.db')
        c = conn.cursor()
        c.execute("INSERT INTO sessions (subject, duration, notes) VALUES (?, ?, ?)",
                  (subject, duration, notes))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:session_id>')
def delete(session_id):
    conn = sqlite3.connect('sessions.db')
    c = conn.cursor()
    c.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:session_id>', methods=['GET', 'POST'])
def edit(session_id):
    conn = sqlite3.connect('sessions.db')
    c = conn.cursor()
    if request.method == 'POST':
        subject = request.form['subject']
        duration = request.form['duration']
        notes = request.form['notes']
        c.execute("UPDATE sessions SET subject=?, duration=?, notes=? WHERE id=?",
                  (subject, duration, notes, session_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        c.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
        session = c.fetchone()
        conn.close()
        return render_template('edit.html', session=session)

if __name__ == '__main__':
    app.run(debug=True)
