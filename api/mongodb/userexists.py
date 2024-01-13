import json
from http.server import BaseHTTPRequestHandler
from bson import ObjectId
from pymongo import MongoClient

def user_exists(username):
    mongoURI = "PRIVATE_MONGODB_URI"
    client = MongoClient(mongoURI)
    db = client["CVMaker"]
    collection = db["users"]
    user = collection.find_one({"username": username})
    client.close()
    return user is not None

class handler(BaseHTTPRequestHandler):

   def do_POST(self):
         content_length = int(self.headers['Content-Length'])
         post_data = self.rfile.read(content_length)
         received_data = str(post_data.decode('utf-8'))
         json_data = json.loads({"boolean": user_exists(received_data)})

         self.send_response(200)
         self.send_header('Content-type', 'application/json')
         self.end_headers()
         self.wfile.write(json_data.encode('utf-8'))