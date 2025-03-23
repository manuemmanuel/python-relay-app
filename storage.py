import json
import os

class LocalStorage:
    def __init__(self):
        self.storage_file = "users.json"
        
        # Create storage file if it doesn't exist
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, "w") as f:
                json.dump({}, f)
    
    def get_users(self):
        try:
            with open(self.storage_file, "r") as f:
                return json.load(f)
        except:
            return {}
    
    def save_users(self, users):
        with open(self.storage_file, "w") as f:
            json.dump(users, f)
    
    def create_user(self, username, password):
        users = self.get_users()
        if username in users:
            return False, "Username already exists"
        
        users[username] = {
            "password": password  # In a real app, you should hash the password
        }
        self.save_users(users)
        return True, "User created successfully"
    
    def verify_user(self, username, password):
        users = self.get_users()
        if username not in users:
            return False, "Invalid username or password"
        
        if users[username]["password"] != password:
            return False, "Invalid username or password"
        
        return True, "Login successful" 