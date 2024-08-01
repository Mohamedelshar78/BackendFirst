from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from typing import Optional
import os

app = Flask(__name__)

try:
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    print(f"MONGO_URI: {app.config.get('MONGO_URI')}")  # Debugging line
    mongo = PyMongo(app)
    print(f"mongo: {mongo}")  # Debugging line
    print(f"mongo.db: {mongo.db}")  # Debugging line
    collection = mongo.db.motorCollection
except Exception as e:
    print(f"Failed to initialize MongoDB: {e}")
# Helper function to convert document to motor
def to_motor(doc):
    """
    Convert a MongoDB document to a dictionary with consistent field names and types.
    """
    def safe_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0
    
    # Convert ObjectId to string
    doc['_id'] = str(doc['_id'])
    
    return {
        "ownerName": doc.get("ownerName", ""),
        "velocity1": safe_float(doc.get("velocity1")),
        "velocity2": safe_float(doc.get("velocity2")),
        "ability1": safe_float(doc.get("ability1")),
        "ability2": safe_float(doc.get("ability2")),
        "weight": safe_float(doc.get("weight")),
        "ble1": doc.get("ble1", ""),
        "ble2": doc.get("ble2", ""),
        "notes": doc.get("notes", ""),
        "division": safe_float(doc.get("division")),
        "motorDiameter1": safe_float(doc.get("motorDiameter1")),
        "motorDiameter2": safe_float(doc.get("motorDiameter2")),
        "lengthOWire": safe_float(doc.get("lengthOWire")),
        "numberOfSewers": safe_float(doc.get("numberOfSewers")),
        "type": doc.get("type", "")
    }

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/add_New_Motore/", methods=['POST'])
def add_New_Motore():
    data = request.json
    print(f"Received data: {data}")
    try:
        result = addNewMotore(
            data.get("ownerName"), data.get("velocity1"), data.get("velocity2"),
            data.get("ability1"), data.get("ability2"), data.get("weight"),
            data.get("ble1"), data.get("ble2"), data.get("notes"),
            data.get("division"), data.get("motorDiameter1"), data.get("motorDiameter2"),
            data.get("lengthOWire"), data.get("numberOfSewers"), data.get("type")
        )
        return jsonify({"message": "Insertion successful" if result else "Insertion failed"})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"detail": str(e)}), 500

@app.route("/get_all/", methods=['GET'])
def get_All():
    try:
        motors = getAllMotores()
        return jsonify(motors)  # Directly return the list of motor objects
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"detail": str(e)}), 500

@app.route("/search_motore/", methods=['GET'])
def search_motore():
    try:
        numer_of_turns = request.args.get('numerOfTurns', type=float)
        diameter = request.args.get('diameter', type=float)
        number_of_sewers = request.args.get('numberOfSewers', type=float)
        
        result = getmotorsBy(numer_of_turns, diameter, number_of_sewers)
        return jsonify(result)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"detail": str(e)}), 500

@app.route("/get_details/", methods=['GET'])
def get_motor_by_owner_and_type():
    owner_name = request.args.get('owner_name')
    motor_type = request.args.get('type')
    
    if not owner_name or not motor_type:
        return jsonify({"detail": "ownerName and type are required parameters"}), 400
    
    try:
        motor = collection.find_one({"ownerName": owner_name, "type": motor_type})
        if motor:
            return jsonify(to_motor(motor))
        else:
            return jsonify({"detail": "Motor not found"}), 404
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"detail": str(e)}), 500

# MongoDB functions
def addNewMotore(ownerName, velocity1, velocity2, ability1, ability2, weight, ble1, ble2, notes, division, motorDiameter1, motorDiameter2, lengthOWire, numberOfSewers, type):
    new_motor = {
        "ownerName": ownerName,
        "velocity1": velocity1,
        "velocity2": velocity2,
        "ability1": ability1,
        "ability2": ability2,
        "weight": weight,
        "ble1": ble1,
        "ble2": ble2,
        "notes": notes,
        "division": division,
        "motorDiameter1": motorDiameter1,
        "motorDiameter2": motorDiameter2,
        "lengthOWire": lengthOWire,
        "numberOfSewers": numberOfSewers,
        "type": type
    }

    try:
        result = collection.insert_one(new_motor)
        return result.inserted_id is not None
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def getAllMotores():
    try:
        motors = list(collection.find())
        return [to_motor(motor) for motor in motors]  # Convert each document to motor format
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def getmotorsBy(numer_of_turns: Optional[float] = None, diameter: Optional[float] = None, number_of_sewers: Optional[float] = None):
    try:
        query = {}
        
        if numer_of_turns is not None:
            query["number_of_turns"] = {"$gte": numer_of_turns, "$lt": numer_of_turns + 1}
        
        if diameter is not None:
            query["motorDiameter1"] = {"$gte": diameter, "$lt": diameter + 1}
        
        if number_of_sewers is not None:
            query["numberOfSewers"] = {"$gte": number_of_sewers, "$lt": number_of_sewers + 1}
        
        motors = list(collection.find(query))
        
        return [to_motor(motor) for motor in motors]  # Convert each document to motor format
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    app.run()
