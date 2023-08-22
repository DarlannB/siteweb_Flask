import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATABASE = 'database.db'  # Use your SQLite database path

def execute_query(query, parameters=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    if parameters:
        cursor.execute(query, parameters)
    else:
        cursor.execute(query)
    
    conn.commit()
    conn.close()

def fetch_all(query):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    result_list = [dict(zip(columns, row)) for row in rows]
    
    conn.close()
    return result_list

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_promotion', methods=['GET', 'POST'])
def create_promotion():
    if request.method == 'POST':
        name = request.form['name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        nationality = request.form['nationality']
        
        query = "INSERT INTO promotion (PromotionName, PromotionStartDate, PromotionEndDate, PromotionNationality) VALUES (?, ?, ?, ?)"
        parameters = (name, start_date, end_date, nationality)
        execute_query(query, parameters)
        
        return redirect(url_for('list_promotions'))
    
    return render_template('create_promotion.html')

@app.route('/promotions')
def list_promotions():
    query = "SELECT * FROM promotion"
    result_list = fetch_all(query)
    return render_template('promotion.html', promotions=result_list)

@app.route('/delete_promotion/<int:promotion_id>', methods=['POST', 'DELETE'])
def delete_promotion(promotion_id):
    if request.method in ['POST', 'DELETE']:
        query = "DELETE FROM promotion WHERE PromotionID = ?"
        parameters = (promotion_id,)
        execute_query(query, parameters)
        
        return redirect(url_for('list_promotions'))

################## PILOTS #################################################

@app.route('/create_pilot', methods=['GET', 'POST'])
def create_pilot():
    if request.method == 'POST':
        name = request.form['PilotName']
        surname = request.form['PilotSurname']
        code_name = request.form['CodeName']
        promotion_id = request.form['promotion']

        query = "INSERT INTO pilot (PromotionID, PilotName, PilotSurname, PilotCodeName) VALUES (?, ?, ?, ?)"
        parameters = (promotion_id, name, surname, code_name)
        execute_query(query, parameters)

        return redirect(url_for('pilotList'))

    return render_template('create_pilot.html', promotions=fetch_all("SELECT * FROM promotion"))

@app.route('/pilot_list')
def pilotList():
    query = "SELECT * FROM pilot"
    result_list = fetch_all(query)
    return render_template('pilot.html', pilots=result_list)

@app.route('/delete_pilot/<int:pilot_id>', methods=['POST', 'DELETE'])
def delete_pilot(pilot_id):
    if request.method in ['POST', 'DELETE']:
        query = "DELETE FROM pilot WHERE PilotID = ?"
        parameters = (pilot_id,)
        execute_query(query, parameters)
        
        return redirect(url_for('pilotList'))

if __name__ == '__main__':
    app.run(debug=True)