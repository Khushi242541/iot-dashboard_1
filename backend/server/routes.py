from flask import Blueprint, request, jsonify
from server.mongo import production_collection, downtime_collection, recipe_collection, item_collection
#Import collection from mongo config
 
#Define Blueprint 
Production = Blueprint("production", __name__)

#POST route to insert production data

@Production.route("/post_production", methods=["POST"])
def post_production():
    data = request.json
    required_fields = ["production1_value1", "production1_value2", "production2_value1", "production2_value2"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400
 
    production_collection.insert_one(data)
    return jsonify({"message": "Data inserted successfully"}), 201


@Production.route("/post_downtime", methods=["POST"])
def post_downtime():
    data = request.json
    required_fields = ["run_time", "process_downtime", "maintenance_dt", "other_downtime"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400

    downtime_collection.insert_one(data)
    return jsonify({"message": "Downtime data inserted successfully"}), 201


# routes.py  ➜  post_recipe
@Production.route("/post_recipe", methods=["POST"])
def post_recipe():
    data = request.json
    required_fields = ["Previous recipe", "Current recipe", "Next recipe"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields"}), 400

    # 🔄 wrap under "recipe"
    recipe_collection.insert_one({"recipe": data})
    return jsonify({"message": "Data inserted successfully"}), 201



@Production.route("/item_list", methods=["GET", "POST"])
def item_list():
    if request.method=="POST":
        data = request.json
        required_fields = ["code","value"]

        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing code and value"})
 
        item_collection.insert_one(data)
        return jsonify({"message": "Data inserted successfully"})
    
    elif request.method=="GET":
        code=request.args.get("code")
        value=request.args.get("value")

    if not code or not value: 
        return jsonify({"error": "Missing code or value"})  
    
    result=item_collection.find_one({"code": code, "value": value})
    if result: 
        result["_id"] = str(result["_id"])
        return jsonify({"item": result}), 200
    else: 
        return jsonify({"error": "Item not found"})


@Production.route("/get_pie_data", methods=["GET"])
def get_pie_data():
    try:
        # Aggregate total values from all documents
        totals = {"run_time": 0, "process_downtime": 0, "maintenance_dt": 0, "other_downtime": 0}

        all_docs = production_collection.find()
        for doc in all_docs:
            for key in totals:
                if key in doc:
                    totals[key] += doc[key]

        labels = list(totals.keys())
        values = list(totals.values())

        return jsonify({"labels": labels, "values": values})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
