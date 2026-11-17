# Functions in file: check_teacher_exists, hash_pass, check_pass, create_teacher, teacher_login, get_all_teachers
# get_all_students, create_student, create_teacher, get_teacher_subjects
# get_student_attendance, get_student_subjects, student_un_enrollment, student_enrollment
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

def get_all_teachers():
    response = supabase.table("teachers").select("*").execute()
    return response.data

def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data

def create_student(new_name, face_embedding, voice_embedding):
    data = {"full_name":new_name, 
            "face_embedding":face_embedding,
            "voice_embedding": voice_embedding}
    response = supabase.table("students").insert(data).execute()
    return response.data

def create_subject(subject_code, sub_name, section, teacher_id):
    data = {"subject_code":subject_code, 
            "name":sub_name,
            "section": section, 
            "teacher_id": teacher_id
            }
    response = supabase.table("subjects").insert(data).execute()
    return response.data

def get_teacher_subjects(teacher_id):
    response = supabase.table("subjects").select("*,subject_students(count), attendance_logs(timestamp)").eq("teacher_id",teacher_id).execute()
    subject = response.data
    for sub in subject:
        sub['total_students'] = sub.get("subject_students",[{}])[0].get('count',0) if sub.get('subject_students') else 0  # check student count data exists
                                    # looks for count key  in the subject_students and if not found return 0 as default, but when no subject_students data found then also return 0
        attendance = sub.get("attendance_logs",[]) 
        unique_sessions = len(set(data['timestamp'] for data in attendance))  # data is a variable name here
                          # counting unique timestamp using set and len , a timestamp from same class share same timestamp, len counts the number of classes
        
        sub['total_classes'] = unique_sessions
        # after counting classes and total_students , the subject_student and attendance_logs data is removed and resulting student dictionary will now be
        # dictionary of (subject_id, subject_name, teacher_id, total_students, total_classes)
        sub.pop('subject_students',None)
        sub.pop('attendance_logs',None)

    return subject

# enroll student to subject
def student_enrollment(student_id, subject_id):
    data = {"student_id":student_id, 
            "subject_id":subject_id
           }
    response = supabase.table("subject_students").insert(data).execute()
    return response.data

# un-enroll student to subject
def student_un_enrollment(student_id, subject_id):
    response = supabase.table("subject_students").delete().eq('student_id',student_id).eq('subject_id',subject_id).execute()
                                                  # delete with a condition otherwise full table will be blown , deletes the enrollment relationship between a student and a subject              
    return response.data

# obtain student id with associated subjects
def get_student_subjects(student_id):
    response = supabase.table("subject_students").select('*,subjects(*)').eq('student_id',student_id).execute()
    return response.data

# get student_attendance
def get_student_attendance(student_id):
    response = supabase.table('attendance_logs').select('*,subjects(*)').eq('student_id',student_id).execute()
    return response.data

def create_attendance(logs):
    response = supabase.table('attendance_logs').insert(logs).execute()
    return response.data