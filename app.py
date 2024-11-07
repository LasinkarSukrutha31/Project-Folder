import json
from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# File path for storing registration data
json_file_path = 'registrations.json'

# Serve the registration form directly from the root directory
@app.route('/')
def index():
    try:
        # Serve the HTML form directly from the current working directory
        return send_from_directory(os.getcwd(), 'RegForm.html')
    except FileNotFoundError:
        return jsonify({'message': 'Registration form not found!'}), 404

# Handle registration data sent from the form (via POST)
@app.route('/register', methods=['POST'])
def register():
    try:
        # Get data from the request (JSON)
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')

        # Validate the data
        if not name or not email or not password or not phone:
            return jsonify({'message': 'All fields are required!'}), 400
        
        # Prepare data to be saved into JSON file
        new_registration = {
            'name': name,
            'email': email,
            'password': password,
            'phone': phone
        }

        # Load existing registrations (if any)
        try:
            with open(json_file_path, 'r') as f:
                registrations = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            registrations = []

        # Append the new registration data to the list
        registrations.append(new_registration)

        # Save the updated list back to the JSON file
        with open(json_file_path, 'w') as f:
            json.dump(registrations, f, indent=4)

        # Respond with a success message
        return jsonify({'message': f'Welcome, {name}! Your registration is complete.'})

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
