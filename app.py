#(database create + table)
import sqlite3

conn = sqlite3.connect("currency.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS exchange_rates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_currency TEXT,
    to_currency TEXT,
    rate REAL
)
""")

# Sample data
rates = [
    ('USD','INR',83.00),
    ('INR','USD',0.012),
    ('USD','EUR',0.92),
    ('EUR','USD',1.08),
    ('USD','GBP',0.79),
    ('GBP','USD',1.27),
]
    

cursor.executemany(
    "INSERT INTO exchange_rates (from_currency, to_currency, rate) VALUES (?, ?, ?)",
    rates
)

conn.commit()
conn.close()

print("Database & table created!")


#FULL backend code
from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convert")
def convert():
    from_currency = request.args.get("from")
    to_currency = request.args.get("to")
    amount = float(request.args.get("amount"))

    conn = sqlite3.connect("currency.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT rate FROM exchange_rates WHERE from_currency=? AND to_currency=?",
        (from_currency, to_currency)
    )
    row = cur.fetchone()
    conn.close()

    if row:
        rate = row[0]
        return jsonify({"converted_amount": amount * rate})
    else:
        return jsonify({"error": "Rate not found"})

if __name__ == "__main__":
    app.run(debug=True)




#Flask ko HTML serve karwana
from flask import render_template

@app.route("/")
def home():
    return render_template("index.html")



#
@app.route("/convert")
def convert():
    from_cur = request.args.get("from")
    to_cur = request.args.get("to")
    amount = float(request.args.get("amount"))
    
    conn = sqlite3.connect("currency.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT rate FROM exchange_rates WHERE from_currency=? AND to_currency=?",
        (from_cur, to_cur)
    )
    row = cur.fetchone()
    conn.close()
    
    if row:
        return jsonify({"converted_amount": amount * row[0]})
    else:
        return jsonify({"error": "Rate not found"})

