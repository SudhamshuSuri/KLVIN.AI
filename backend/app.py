from flask import Flask, request
from flask_cors import CORS
from models import fetch_companies, fetch_devices
from utils import create_response

app = Flask(__name__)
CORS(app)

@app.route('/api/companies', methods=['GET'])
def get_companies():
    try:
        companies = fetch_companies()
        return create_response(companies)
    except Exception as e:
        return create_response({"error": str(e)}, status=500)

@app.route('/api/companies/<int:company_id>/devices', methods=['GET'])
def get_devices(company_id):
    try:
        devices = fetch_devices(company_id)
        return create_response(devices)
    except Exception as e:
        return create_response({"error": str(e)}, status=500)

if __name__ == '__main__':
    app.run(debug=True)

