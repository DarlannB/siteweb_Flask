import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATABASE = 'database.db'  # Use your SQLite database path

@app.route('/')
def index():
    return render_template('index.html')

################## PROMOTION #################################################

@app.route('/create_promotion', methods=['GET'])
def createPromotion():
    return render_template('create_promotion.html')

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


@app.route('/promotions', methods=['GET'])
def list_promotions():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM promotion")
    
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    result_list = [dict(zip(columns, row)) for row in rows]

    conn.close()

    return render_template('promotion.html', promotions=result_list)

@app.route('/delete_promotion/<int:promotion_id>', methods=['POST', 'DELETE'])
def delete_promotion(promotion_id):
    if request.method == 'POST' or request.method == 'DELETE':
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM promotion WHERE PromotionID = ?", (promotion_id,))
        conn.commit()
        conn.close()

        return redirect(url_for('list_promotions'))
    
################## PILOTS #################################################

@app.route('/create_pilot', methods=['POST'])
def create_pilot():
    PiloteName = request.form['Name']
    PiloteSurname = request.form['Surname']
    Pilotecode_name =  request.form['Code Name']
    Promotion = request.form['Promotion']
    Group = request.form['Group']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO pilot (PiloteName, PiloteSurname, PiloteCodeName, Group, Promotion) VALUES (?, ?, ?)",
                   (PiloteName, PiloteSurname, Pilotecode_name, Group, Promotion))
    pilot_id = cursor.lastrowid  # Get the ID of the inserted pilot

    # Link the pilot to the selected promotion
    cursor.execute("INSERT INTO pilot_promotion (PilotID, PromotionID) VALUES (?, ?)", (pilot_id, promotion_id))

    conn.commit()
    conn.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)