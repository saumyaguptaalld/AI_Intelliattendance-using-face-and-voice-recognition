from src.database.config import supabase
import bcrypt

def check_teacher_exists(username):
     # check for unique username, returns false if username is already taken
    response = supabase.table("teachers").select("username").eq("username",username).execute()
    return len(response.data) > 0   # returns true is teacher exists in database

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode("utf-8"),bcrypt.gensalt()).decode("utf-8") # encode converts string to raw bytes(crypt), gensalt creates random cryptographic string called salt, decode turns the generated salt bytes to text string, The salt makes the resulting hash different even when two users have the same password.
                         # pwd.encode mixes the byte version of password and salt together, # decode converts the final secure hash to clean text stringfor saving in database text column
def check_pass(pwd, hashedpwd):
    return bcrypt.checkpw(pwd.encode(),hashedpwd.encode()) 

def create_teacher(username, password, name):
    data = {"username":username, 
            "password":hash_pass(password),
            "name": name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data

def teacher_login(username, password):
    response = supabase.table("teachers").select('*').eq("username",username).execute()
    if not response.data:
        return None

    if response.data:
        teacher = response.data[0]
        
        if check_pass(password, teacher["password"]):
            return {
            "teacher_id": teacher["teacher_id"],
            "username": teacher["username"],
            "name": teacher["name"],
            }
    return None

def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data