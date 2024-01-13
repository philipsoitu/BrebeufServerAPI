import json
from http.server import BaseHTTPRequestHandler
from bson import ObjectId
from pymongo import MongoClient

def modify_user_cv_data(username, cv_data):
    mongoURI = "PRIVATE_MONGODB_URI"
    client = MongoClient(mongoURI)
    db = client["CVMaker"]
    collection = db["users"]


    # Update the cv_data for the user with the specified ObjectId
    result = collection.update_one({"username": username}, {"$set": {"cv_data": cv_data}})

    # Check if the update was successful
    if result.modified_count > 0:
        return True
    else:
        return False
    
class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        received_data = str(post_data.decode('utf-8'))
        
        json_data = json.loads(received_data)
        
        username = json_data.get('username', '')
        cv_data = json_data.get('cv_data', '')
        
        result = modify_user_cv_data(username, cv_data)
        
        response_data = json.dumps(result)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response_data.encode('utf-8'))

        {"username": username, "cv_data":cv_data}