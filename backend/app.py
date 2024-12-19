from flask import Flask, request
from flask_cors import CORS
from models import fetch_companies, fetch_devices
from utils import create_response
from flask import Flask, jsonify, request
from models import fetch_companies, add_device


app = Flask(__name__)
CORS(app, resources=r"/*")

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

@app.route('/api/devices', methods=['POST'])
def create_device():
    """Add a new device."""
    try:
        data = request.json
        device_name = data.get('name')
        company_id = data.get('company_id')

        if not device_name or not company_id:
            return jsonify({"error": "Device name and company ID are required"}), 400

        # Add the device to the database
        add_device(device_name, company_id)
        return jsonify({"message": "Device added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

