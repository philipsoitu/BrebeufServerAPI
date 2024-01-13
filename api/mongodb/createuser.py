import json
from http.server import BaseHTTPRequestHandler
from bson import ObjectId
from pymongo import MongoClient

def create_user(name, username, password):
    mongoURI = "mongodb+srv://philipsoitu:Iozgg5ms9TR7eZI0@cluster0.8smo8s6.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(mongoURI)
    db = client["CVMaker"]
    collection = db["users"]
    user_data = {
        "name": name,
        "username": username,
        "password": password,
        "referral_code": collection.count_documents({})+1,
        "referral_points": 0,
        "cv_data": "",
        "events": []
    }
    collection.insert_one(user_data)
    
    return "success"

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        received_data = str(post_data.decode('utf-8'))
        
        json_data = json.loads(received_data)
        
        name = json_data.get('name', '')
        username = json_data.get('username', '')
        password = json_data.get('password', '')
        
        result = create_user(name, username, password)
        
        response_data = json.dumps(result)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response_data.encode('utf-8'))