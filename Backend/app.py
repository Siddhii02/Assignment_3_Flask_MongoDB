from flask import Flask, request,jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import certifi
import os,json

# Load env variables
load_dotenv()
uri=os.getenv("MONGO_URI")

# connect to mongo db
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
print(client.list_database_names())
db=client['testdb']
collection=db['flask-tuturial']
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Mongo connection error",e)

app=Flask(__name__)

@app.route('/api',methods=['GET'])
def api_data():
    try:
        with open("data.json",'r') as f:
            data=json.load(f)
        return jsonify(data)
    except Exception as  e:
        return jsonify({"error":str(e)})
    
@app.route('/submit', methods=['POST'])
def submit():
    try:
        form_data=dict(request.json)
        collection.insert_one(form_data)
        return "Data submitted successfully",200
    except Exception as e:
        return f"Error : {str(e)}, 400"

    
@app.route('/view',methods=['GET'])
def view():
    data=list(collection.find())
    for item in data:
        item.pop("_id", None)
    return jsonify({"data":data})

if __name__ == "__main__":
    app.run(port=9000, debug=True, use_reloader=False)