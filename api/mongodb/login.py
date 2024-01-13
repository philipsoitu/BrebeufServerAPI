import json
from http.server import BaseHTTPRequestHandler
from bson import ObjectId
from pymongo import MongoClient

def login(username, password):
    mongoURI = "PRIVATE_MONGODB_URI"
    client = MongoClient(mongoURI)
    db = client["CVMaker"]
    collection = db["users"]

    user_document = collection.find_one({"username": username, "password": password}, {"_id": 1})

    if user_document:
        return user_document["_id"]
    else:
        return None
    
class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        received_data = str(post_data.decode('utf-8'))
        
        json_data = json.loads(received_data)
        
        username = json_data.get('username', '')
        password = json_data.get('password', '')
        
        result = login(username, password)
        
        response_data = json.loads({"boolean": result})
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response_data.encode('utf-8'))