from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory storage for users
users = {}
user_id_counter = 1

# Helper function to validate user data
def validate_user_data(data, required_fields=None):
    if required_fields is None:
        required_fields = ['name', 'email']
    
    errors = []
    
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"{field} is required")
    
    if 'email' in data and '@' not in data['email']:
        errors.append("Invalid email format")
    
    return errors

# GET /users - Retrieve all users
@app.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    return jsonify({
        "status": "success",
        "data": list(users.values()),
        "count": len(users)
    }), 200

# GET /users/<id> - Retrieve a specific user
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    if user_id not in users:
        return jsonify({
            "status": "error",
            "message": "User not found"
        }), 404
    
    return jsonify({
        "status": "success",
        "data": users[user_id]
    }), 200

# POST /users - Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    global user_id_counter
    
    # Get JSON data from request
    data = request.get_json()
    
    if not data:
        return jsonify({
            "status": "error",
            "message": "No data provided"
        }), 400
    
    # Validate required fields
    errors = validate_user_data(data)
    if errors:
        return jsonify({
            "status": "error",
            "message": "Validation failed",
            "errors": errors
        }), 400
    
    # Check if email already exists
    for user in users.values():
        if user['email'] == data['email']:
            return jsonify({
                "status": "error",
                "message": "Email already exists"
            }), 409
    
    # Create new user
    new_user = {
        "id": user_id_counter,
        "name": data['name'],
        "email": data['email'],
        "age": data.get('age'),
        "phone": data.get('phone'),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    users[user_id_counter] = new_user
    user_id_counter += 1
    
    return jsonify({
        "status": "success",
        "message": "User created successfully",
        "data": new_user
    }), 201

# PUT /users/<id> - Update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user"""
    if user_id not in users:
        return jsonify({
            "status": "error",
            "message": "User not found"
        }), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            "status": "error",
            "message": "No data provided"
        }), 400
    
    # Validate data if name or email are being updated
    required_fields = []
    if 'name' in data:
        required_fields.append('name')
    if 'email' in data:
        required_fields.append('email')
    
    if required_fields:
        errors = validate_user_data(data, required_fields)
        if errors:
            return jsonify({
                "status": "error",
                "message": "Validation failed",
                "errors": errors
            }), 400
    
    # Check if email already exists (excluding current user)
    if 'email' in data:
        for uid, user in users.items():
            if uid != user_id and user['email'] == data['email']:
                return jsonify({
                    "status": "error",
                    "message": "Email already exists"
                }), 409
    
    # Update user fields
    user = users[user_id]
    updatable_fields = ['name', 'email', 'age', 'phone']
    
    for field in updatable_fields:
        if field in data:
            user[field] = data[field]
    
    user['updated_at'] = datetime.now().isoformat()
    
    return jsonify({
        "status": "success",
        "message": "User updated successfully",
        "data": user
    }), 200

# DELETE /users/<id> - Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    if user_id not in users:
        return jsonify({
            "status": "error",
            "message": "User not found"
        }), 404
    
    deleted_user = users.pop(user_id)
    
    return jsonify({
        "status": "success",
        "message": "User deleted successfully",
        "data": deleted_user
    }), 200

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "success",
        "message": "API is running",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500

if __name__ == '__main__':
    users[1] = {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
        "phone": "+1234567890",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    users[2] = {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane@example.com",
        "age": 25,
        "phone": "+1987654321",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    user_id_counter = 3
    
    print("Starting User Management API...")
    print("Available endpoints:")
    print("  GET    /users       - Get all users")
    print("  GET    /users/<id>  - Get specific user")
    print("  POST   /users       - Create new user")
    print("  PUT    /users/<id>  - Update user")
    print("  DELETE /users/<id>  - Delete user")
    print("  GET    /health      - Health check")
    
    app.run(debug=True, host='0.0.0.0', port=5000)