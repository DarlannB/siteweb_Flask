import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATABASE = 'database.db'  # Use your SQLite database path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_promotion', methods=['POST'])
def create_promotion():
    name = request.form['name']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    nationality = request.form['nationality']

    try:
        db = sqlite3.connect(DATABASE)
        db.execute("INSERT INTO promotion (PromotionName, PromotionStartDate, PromotionEndDate, PromotionNationality) VALUES (?, ?, ?, ?)",
                (name, start_date, end_date, nationality))
        db.commit()
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        db.close()

    return redirect(url_for('list_promotions'))

@app.route('/promotions')
def list_promotions():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM promotion")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    result_list = [dict(zip(columns, row)) for row in rows]

    conn.close()

    return render_template('promotion.html', promotions=result_list)

if __name__ == '__main__':
    app.run(debug=True)