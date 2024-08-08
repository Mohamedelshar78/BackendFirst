from flask import Flask, request, jsonify
from pymongo import MongoClient
from typing import Optional
import os

app = Flask(__name__)


client = MongoClient(os.getenv("MONGO_URI"))
db = client['motor_db']
collection = db['motorCollection']

# Helper function to convert document to motor
def to_motor(doc):
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
        "lengthOfTheWire": safe_float(doc.get("lengthOfTheWire")),
        "numberOfSewers": safe_float(doc.get("numberOfSewers")),
        "numberOfTurns": (doc.get("numberOfTurns")),
        "type": doc.get("type", ""),
        "wrappedCountry": doc.get("wrappedCountry", False),
        "steps": doc.get("steps",""),
        "step": doc.get("step",""),
        "stepTquem": doc.get("stepTquem",""),
        "wireThickness": doc.get("wireThickness",""),
        "numberOfTurnsTquem": doc.get("numberOfTurnsTquem",""),
        "wireThicknessTquem": doc.get("wireThicknessTquem",""),
        "waterpump": doc.get("waterpump", False),
        "lengthOfMobina":safe_float(doc.get("lengthOfMobina")),
        "diameterOfMobina":safe_float(doc.get("diameterOfMobina")),
        "divisionMobina":(doc.get("divisionMobina","")),
        "numberOfTurnsMobina":(doc.get("numberOfTurnsMobina","")),
        "numberOfSewersMobina":safe_float(doc.get("numberOfSewersMobina")),
        "wireThicknessMobina":(doc.get("wireThicknessMobina","")),
        "weightMobina":safe_float(doc.get("weightMobina")),
        "stepMobina": doc.get("stepMobina", ""),
        "velocityMobina":safe_float(doc.get("velocityMobina")),
        "abilityMobina":safe_float(doc.get("abilityMobina")),




        
        
    }

@app.route('/')
def hello_world():
    return 'Hello, World!'



@app.route("/add_MotorSeliPring/", methods=['POST'])
def add_MotorSeliPring():
    data = request.json
    print(f"Received data: {data}")
    try:
        result = addNewMotoreSeliPring(
            data["type"], data["ownerName"], data["velocity1"], data["velocity2"],
            data["ability1"], data["ability2"], data["weight"], data["ble1"], 
            data["ble2"], data["notes"], data["division"], data["motorDiameter1"], 
            data["motorDiameter2"], data["lengthOfTheWire"], data["numberOfSewers"], 
            data["numberOfTurns"], data["step"],data["lengthOfMobina"],
            data["diameterOfMobina"],data["divisionMobina"],data["numberOfTurnsMobina"],
            data["numberOfSewersMobina"],data["wireThicknessMobina"],data["weightMobina"],
            data["stepMobina"],data["velocityMobina"],data["abilityMobina"]
        )
        return jsonify({"message": "Insertion successful" if result else "Insertion failed"})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"detail": str(e)}), 500

@app.route("/add_Motor3Phase/", methods=['POST'])
def add_Motor3Phase():
    data = request.json
    print(f"Received data: {data}")
    try:    
        result = addNew3Pase(
            data.get("step"),
            data.get("type"), data.get("ownerName"), data.get("velocity1"), data.get("velocity2"),
            
            data.get("ability1"), data.get("ability2"), data.get("weight"),
            
            data.get("ble1"), data.get("ble2"), data.get("notes"),
            
            data.get("division"), data.get("motorDiameter1"), data.get("motorDiameter2"),
            
            data.get("lengthOfTheWire"), data.get("numberOfSewers"), data.get("numberOfTurns"),
            
            data.get("wireThickness"),data.get("wrappedCountry"),data.get("waterpump")
            
            
        )
        return jsonify({"message": "Insertion successful" if result else "Insertion failed"})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"detail": str(e)}), 500

@app.route("/add_Motor220Volt/", methods=['POST'])
def add_Motor220Volt():
    data = request.json

    print(f"Received data: {data}")
    try:
        result = addNew220Volt(
            data.get("type"), data.get("ownerName"), data.get("velocity1"), data.get("velocity2"),
            data.get("weight"), data.get("ble1"), data.get("ble2"), data.get("notes"),
            data.get("division"), data.get("motorDiameter1"), data.get("motorDiameter2"),
            data.get("lengthOfTheWire"), data.get("wrappedCountry"), data.get("step"),
            data.get("wireThickness"),data.get("numberOfTurns"),  data.get("stepTquem"),
            data.get("numberOfTurnsTquem"), data.get("wireThicknessTquem")
        )
        return jsonify({"message": "Insertion successful" if result else "Insertion failed"})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"detail": str(e)}), 500


@app.route("/get_all/", methods=['GET'])
def get_all():
    try:
        motors = getAllMotors()
        return jsonify(motors)
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

@app.route("/search_motor/", methods=['GET'])
def search_motor():
    try:
        number_of_turns = request.args.get('numberOfTurns', type=float)
        diameter = request.args.get('diameter', type=float)
        number_of_sewers = request.args.get('numberOfSewers', type=float)
        
        result = getMotorsBy(number_of_turns, diameter, number_of_sewers)
        return jsonify(result)
    except Exception as e:
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
        return jsonify({"detail": str(e)}), 500

# MongoDB functions
def addNewMotoreSeliPring(type, ownerName, velocity1, velocity2, ability1, ability2, weight, ble1, ble2, notes,
                          division, motorDiameter1, motorDiameter2, lengthOfTheWire, numberOfSewers, numberOfTurns, step,
                          lengthOfMobina,diameterOfMobina,divisionMobina,numberOfTurnsMobina,
                          numberOfSewersMobina,wireThicknessMobina,weightMobina,stepMobina,velocityMobina,abilityMobina):
    new_motor = {
        "type": type,
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
        "lengthOfTheWire": lengthOfTheWire,
        "numberOfTurns": numberOfTurns,
        "numberOfSewers": numberOfSewers,
        "steps": step,
        "lengthOfMobina":lengthOfMobina,
        "diameterOfMobina":diameterOfMobina,
        "divisionMobina":divisionMobina,
        "numberOfTurnsMobina":numberOfTurnsMobina,
        "numberOfSewersMobina":numberOfSewersMobina,
        "wireThicknessMobina":wireThicknessMobina,
        "weightMobina":weightMobina,
        "stepMobina":stepMobina,
        "velocityMobina":velocityMobina,
        "abilityMobina":abilityMobina
    }

    try:
        result = collection.insert_one(new_motor)
        return result.inserted_id is not None
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def addNew3Pase(step,type, ownerName, velocity1, velocity2, ability1,ability2, weight, ble1, ble2, notes, 
                division, motorDiameter1, motorDiameter2, lengthOfTheWire, numberOfSewers, numberOfTurns,wireThickness, wrappedCountry, waterpump):
    
    new_motor = {
        "step":step,
        "type": type,
        
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
        
        "lengthOfTheWire": lengthOfTheWire,
        "numberOfSewers": numberOfSewers,
        "numberOfTurns": numberOfTurns,
        
        "wireThickness":wireThickness,
        "wrappedCountry": wrappedCountry,
        "waterpump": waterpump
    }

    try:
        result = collection.insert_one(new_motor)
        return result.inserted_id is not None
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def addNew220Volt(type, ownerName, velocity1, velocity2, weight, ble1, ble2, notes, division, motorDiameter1, motorDiameter2, lengthOfTheWire, wrappedCountry, step, wireThickness, numberOfTurns, stepTquem, numberOfTurnsTquem, wireThicknessTquem):
    new_motor = {
        "type": type,
        "ownerName": ownerName,
        "velocity1": velocity1,
        "velocity2": velocity2,
        "weight": weight,
        "ble1": ble1,
        "ble2": ble2,
        "notes": notes,
        "division": division,
        "motorDiameter1": motorDiameter1,
        "motorDiameter2": motorDiameter2,
        "lengthOfTheWire": lengthOfTheWire,
        "wrappedCountry": wrappedCountry,
        "step": step,
        "wireThickness": wireThickness,
        "numberOfTurns": numberOfTurns,
        "stepTquem": stepTquem,
        "numberOfTurnsTquem": numberOfTurnsTquem,
        "wireThicknessTquem": wireThicknessTquem
    }

    try:
        result = collection.insert_one(new_motor)
        return result.inserted_id is not None
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def getAllMotors():
    try:
        motors = list(collection.find())
        return [to_motor(motor) for motor in motors]
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def getMotorsBy(number_of_turns: Optional[float] = None, diameter: Optional[float] = None, number_of_sewers: Optional[float] = None):
    try:
        query = {}
        
        if number_of_turns is not None:
            query["numberOfTurns"] = {"$gte": number_of_turns, "$lt": number_of_turns + 1}
        
        if diameter is not None:
            query["motorDiameter1"] = {"$gte": diameter, "$lt": diameter + 1}
        
        if number_of_sewers is not None:
            query["numberOfSewers"] = {"$gte": number_of_sewers, "$lt": number_of_sewers + 1}
        
        motors = list(collection.find(query))
        return [to_motor(motor) for motor in motors]
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    app.run()
