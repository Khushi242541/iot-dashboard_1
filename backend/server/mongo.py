from pymongo import MongoClient

# MongoDB Setup
def get_mongo_connection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["TrialGUI"]
    return db

db = get_mongo_connection()
production_collection = db["production_data"]
downtime_collection = db["graphdata"]
recipe_collection = db["recipe_data"]
item_collection = db["Item List"]
piechart_collection=db["pie_data"]

def fetch_production_data():
    db = get_mongo_connection()
    collection = db["production_data"] 
    latest_doc = collection.find_one(sort=[("_id", -1)])      
    if latest_doc:
        return {
            "p1v1": latest_doc.get("production1_value1", 0),
            "p1v2": latest_doc.get("production1_value2", 0),
            "p2v1": latest_doc.get("production2_value1", 0),
            "p2v2": latest_doc.get("production2_value2", 0),
        }
    else:
        return None

 #######For 1 doc insertion only in the table    
# def fetch_recipe_data():
#     db = get_mongo_connection()
#     collection = db["recipe_data"]

#     # Correct way to get the latest document
#     latest_doc = collection.find_one(sort=[("_id", -1)])

#     if latest_doc and "recipe" in latest_doc:
#         recipe = latest_doc["recipe"] 
#         return {
#             "previous": recipe.get("Previous recipe", 0),
#             "current": recipe.get("Current recipe", 0),
#             "next": recipe.get("Next recipe", 0)
#         }
#     else:
#         return None

#####For multiple insertion in the table 
def fetch_recipe_data():
    db = get_mongo_connection()
    collection = db["recipe_data"]

    latest_docs = collection.find().sort("_id", -1).limit(5)

    recipe_list = []
    for doc in latest_docs:
        recipe_doc = doc.get("recipe", doc)
        recipe_list.append({
            "previous": recipe_doc.get("Previous recipe", "N/A"),
            "current": recipe_doc.get("Current recipe", "N/A"),
            "next":    recipe_doc.get("Next recipe", "N/A")
        })

    return recipe_list

    
def fetch_graphdata():
    db = get_mongo_connection()

    ## verifying the connection status 
    print("✅ Connected to MongoDB database:", db.name)
    print("Collections:", db.list_collection_names())

    collection = db["graphdata"]
    latest_doc = collection.find_one(sort=[("_id", -1)])
    print("Fetched from MongoDB:", latest_doc)
    return latest_doc
 
#BOM item list data scrollbar list 
def fetch_continuous_data():
    db = get_mongo_connection()
    collection = db["Item List"]  

    # data = list(collection.find({}, {"_id": 0}))  # Exclude _id if not needed
    # collection.find({}, {"_id": 0}).sort("_id", -1).limit(20)
    data= list(collection.find({}, {"_id": 0}).sort("_id", -1).limit(20))
    return data

def fetch_pie_chart():
  
    return db

# Optional: For testing
if __name__ == "__main__":
    print(fetch_production_data())
    print(fetch_recipe_data())
    print(fetch_graphdata())
    print(fetch_continuous_data())
    print(fetch_pie_chart())  