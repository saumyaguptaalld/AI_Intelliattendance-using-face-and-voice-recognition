import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students

# Describing all dlib models detector, face landmarks, face recognizer
@st.cache_resource
def load_dlib_models():
    # Detector (bounding box)
    detector = dlib.get_frontal_face_detector()  # No of faces and their location

    # landmark
    sp =dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()  # give landmarks location
    )
    # face recognizer
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    return detector, sp, facerec

# we obtain face embeddings of all the faces present in the image
#  (we use numpy image that we obtained at student portal)
# Return one 128-D face embedding for each detected face.
def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()  # Call the face boundary, landmark detector and recognizer model 
    faces = detector(image_np, 1)  # detect all faces in image using detector, 1 means process only once
    encodings = []
    for face in faces: # for a single face in faces
        shape = sp(image_np, face)  # get the face landmarks for that particular face
        face_descriptor = facerec.compute_face_descriptor(image_np,shape, 1)  # get face description for that particluar face
        encodings.append(np.asarray(face_descriptor, dtype=np.float64))  # embeddings 128D values are stored as np array
    return encodings

# all students from database are obtained and fitted/training using support vector classifier
# svc takes two inputs embedding and id that we describe here as x and y
@st.cache_resource    # reuse the cached classifier instead of loading or creating it again.(avoid repeatedly training the SVC classifier during Streamlit reruns)
def get_trained_model():
    student_db = get_all_students()  # retrieves student record from database
    if not student_db:
        return None

    X = [] # input features: student face embeddings
    Y = [] # target_labels: student id
    
    for student in student_db :
        # we get the embeddings of each face stored in database
        embedding = student.get("face_embedding")    # retrieve face embedding from database
        student_id = student.get("student_id")
        if embedding:                   # check if embedding exists
            X.append(np.array(embedding))            # convert embedding to numpy array
            Y.append(int(student_id))        # add corresponding id to y
    if len(X) == 0:  # if we donot get any embedding with the associated face
        return 0     
    
    # classifier for classification
    clf = SVC(kernel='linear', probability=True, class_weight='balanced') # class weight balanced: adjusts class weights inversely according to class frequencies, which can help when the training dataset has unequal numbers of samples per student.

    try:
        clf.fit(X,Y)
    except ValueError as e:
        print(f"Classifier training is failed:{e}") # ensures, a failed training do not return a valid classifier dictionary.
        return None
    return {'clf':clf, 'X':X, "Y":Y}  # returns model and training data

def train_classifier():            
        # Clear only, function's cached result.
        get_trained_model.clear()  # This is used when we do a new student entry 
        # cache invalidation strategy
        model_data = get_trained_model()
        return bool(model_data)  # if new data has come , the train classifier return true

def predict_attendance(class_image_np):  # takes input the class group photo
        encodings = get_face_embeddings(class_image_np)  # get face embeddings of all the faces in the class image
        detected_student = {}      # initialize the detected students
        model_data = get_trained_model() # we get our trained model data

        if not model_data:
            return detected_student, [], len(encodings) # if there is no trained data available, we return the empty detected student dict, empty embedding list [] and the number of students as len(encodings)

        clf = model_data['clf']  # obtain classifier from model data
        X_train = model_data['X']  # obtain face embeddings 
        Y_train = model_data['Y']  # obtain student id from model or trained data 

        all_students = sorted(list(set(Y_train))) # getting all students and using set to get unique students

        for encoding in encodings:  # the encodings obtained from the class photo of all the students, is picked one by one
            if len(all_students) >=2:
                  predicted_id = int(clf.predict([encoding])[0])  # if more than one student , then using classifier we predict which student is it
            else:
                  predicted_id = int(all_students[0]) # the one with max score is saved as predicted id

            student_embedding = X_train[Y_train.index(predicted_id)] # get the embedding of the predicted id from the training 
            # mathematically confirming the embedding obtained for the student is the same student being identified
            best_match_score = np.linalg.norm(student_embedding - encoding)
            resemblance_threshold = 0.6
            if best_match_score <= resemblance_threshold:
                detected_student[predicted_id] = True
        return detected_student, all_students, len(encodings)