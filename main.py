from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)
port = 5000

users = [
    {
        "id": "8a169ade-2d06-4508-b5ba-57e730bef4af",
        "name": "John",
        "age": 20,
        "phone": "123-456-7890",
        "street": "123 Main St",
        "city": "Miami",
    },
    {
        "id": "ef3347db-d6f3-46ac-84aa-36f4c6076cc3",
        "name": "Jane",
        "age": 22,
        "phone": "334-159-2123",
        "street": "123 Hook St",
        "city": "New York",
    },
]

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

@app.route('/users/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = None
    for existing_user in users:
        if existing_user["id"] == user_id:
            user = existing_user
            break
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user), 200
        
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    for key in ['name', 'age', 'phone', 'street', 'city']:
        if key not in data:
            return jsonify({"message": "Bad request, name or age or phone or street or city not found"}), 400
    
    new_user = {
        "id": str(uuid.uuid4()),
        "name": data['name'],
        "age": data['age'],
        "phone": data['phone'],
        "street": data['street'],
        "city": data['city'],
    }
    users.append(new_user)
    return jsonify(new_user), 201


@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    
    user = None
    for existing_user in users:
        if existing_user["id"] == user_id:
            user = existing_user
            break

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json
  
    for key in ['name', 'age', 'phone', 'street', 'city']:
        if key not in data:
            return jsonify({"message": "Bad request, name or age or phone or street or city not found"}), 400

    user.update({
        "name": data['name'],
        "age": data['age'],
        "phone": data['phone'],
        "street": data['street'],
        "city": data['city'],
    })

    return jsonify(user), 200


@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = None
    for existing_user in users:
        if existing_user["id"] == user_id:
            user = existing_user
            break

    if not user:
       return jsonify({"message": "User not found"}), 404
    
    users.remove(user)
    return jsonify({"message": "User successfully deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)