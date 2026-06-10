from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests
import whois
import json
from datetime import datetime
import os
from shodan import Shodan
from config import Config
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Initialize Shodan
shodan_api = None
if Config.SHODAN_API_KEY:
    try:
        shodan_api = Shodan(Config.SHODAN_API_KEY)
        print("✅ Shodan API connected successfully")
    except Exception as e:
        print(f"⚠️ Shodan connection failed: {e}")

class OSINTResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    whois_data = db.Column(db.Text)
    subdomains = db.Column(db.Text)
    shodan_data = db.Column(db.Text, nullable=True)   # Made nullable for safety
    notes = db.Column(db.Text)

# Create / Update tables
with app.app_context():
    db.create_all()
    print("✅ Database initialized successfully")

@app.route('/')
def index():
    history = OSINTResult.query.order_by(OSINTResult.timestamp.desc()).limit(10).all()
    return render_template('index.html', history=history)

@app.route('/scan', methods=['POST'])
def scan():
    target = request.form.get('target', '').strip()
    if not target:
        return "Target is required", 400

    result = {"target": target, "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}

    # WHOIS
    try:
        w = whois.whois(target)
        result["whois"] = {
            "registrar": str(getattr(w, 'registrar', 'N/A')),
            "creation_date": str(getattr(w, 'creation_date', 'N/A')),
            "expiration_date": str(getattr(w, 'expiration_date', 'N/A')),
            "name_servers": getattr(w, 'name_servers', [])
        }
    except Exception as e:
        result["whois"] = {"error": str(e)}

    # Subdomains
    try:
        url = f"https://crt.sh/?q=%25.{target}&output=json"
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            subdomains = sorted(list(set([entry['name_value'].lower() for entry in data if target.lower() in entry['name_value']])))[:50]
            result["subdomains"] = subdomains
    except:
        result["subdomains"] = []

    # Shodan
    shodan_result = {"error": "Shodan not available"}
    if shodan_api:
        try:
            data = shodan_api.search(f'hostname:{target}')
            shodan_result = {
                "total": data.get('total', 0),
                "matches": data.get('matches', [])[:8]
            }
        except Exception as e:
            shodan_result = {"error": str(e)}
    result["shodan"] = shodan_result

    # Save to DB
    db_entry = OSINTResult(
        target=target,
        whois_data=json.dumps(result.get("whois", {})),
        subdomains=json.dumps(result.get("subdomains", [])),
        shodan_data=json.dumps(shodan_result)
    )
    db.session.add(db_entry)
    db.session.commit()

    return render_template('results.html', result=result)

if __name__ == '__main__':
    print("🚀 Starting OSINT Dashboard on http://127.0.0.1:5000")
    app.run(debug=True)