import io
from django.shortcuts import render
from .models import Customer
import cv2
import io
import numpy as np
from PIL import Image
import face_recognition
# Create your views here.


def index(request):
    return render(request, 'index.html')


def compare(image1_data, image2_data):
    # Convert binary data to PIL image
    image1 = Image.open(io.BytesIO(image1_data))
    image2 = Image.open(io.BytesIO(image2_data))

    # Convert PIL image to numpy array
    face1 = np.array(image1)
    face2 = np.array(image2)

    # Convert the images to RGB format
    face1 = cv2.cvtColor(face1, cv2.COLOR_BGR2RGB)
    face2 = cv2.cvtColor(face2, cv2.COLOR_BGR2RGB)
    # Get the face encodings for each face
    face1_encoding = face_recognition.face_encodings(face1)[0]
    face2_encoding = face_recognition.face_encodings(face2)[0]

    # Compare faces
    results = face_recognition.compare_faces([face1_encoding], face2_encoding)

    return results[0]



def profile(request):
    name = request.POST['name']
    face_id_name = request.FILES['face-id'].name
    face_id_file = request.FILES['face-id'].read()

    request.session['name'] = name
    records = {
        'name': name,
        'face_id_name': face_id_name,
        'face_id_file': face_id_file,
        'is_matched': False
    }
    Customer.insert_one(records)
    return render(request, 'profile.html', {'name': name})


def verification(request):
    name = request.session.get('name')

    # digital_id
    if request.method == 'POST':
        digital_id_name = request.FILES['digital-id'].name
        digital_id_file = request.FILES['digital-id'].read()

        prev = {"name": name}
        # Update the digital_id of the existing customer object
        add = {"$set": {"digital_id_name": digital_id_name}}
        Customer.update_one(prev, add)
        add = {"$set": {"digital_id_file": digital_id_file}}
        Customer.update_one(prev, add)

        face_id_file = Customer.find_one(
            {"name": name}, {"face_id_file": 1, "_id": 0})

        face_id_value = list(face_id_file.values())[0]

        # print(type(digital_id_file))
        # print(type(face_id_value))
        if (compare(face_id_value, digital_id_file)):
            add = {"$set": {"is_matched": True}}
            Customer.update_one(prev, add)
            return render(request, 'verified.html', {'name': name})
        else:
            return render(request, 'not_verified.html', {'name': name})
