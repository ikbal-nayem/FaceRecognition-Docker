import os
import joblib
from urllib.request import urlopen
from PIL import Image
from algo.face_recognition.preprocessing import ExifOrientationNormalize
from CONF import firebaseConfig, store_token, PRETRAINED_MODEL_PATH
import pyrebase


class Recognizer():
    def __init__(self):
        # firebase = pyrebase.initialize_app(firebaseConfig)
        # storage = firebase.storage()
        # url = storage.child('model/face_recogniser.pkl').get_url(store_token)
        # self.face_recogniser = joblib.load(urlopen(url))
        self.loadModel()
        self.preprocess = ExifOrientationNormalize()

    def loadModel(self):
        self.has_trained = True
        file_loc = os.path.join(os.getcwd(), PRETRAINED_MODEL_PATH)
        if not os.path.exists(file_loc):
            self.has_trained = False
        if self.has_trained:
            self.face_recogniser = joblib.load(file_loc)

    def recognize(self, img):
        img = img.convert('RGB')
        img = self.preprocess(img)
        faces = self.face_recogniser(img)
        return [{
                'top_prediction': face['top_prediction'],
                'bounding_box': face['bb']
                } for face in faces]

    def applyWithURL(self, img_url):
        if self.has_trained:
            image = Image.open(urlopen(img_url))
            faces = self.recognize(image)
            return {"success": True, "faces": faces}
        return {"success": False, "message": "Data is not trained yet."}

    def applyWithImg(self, img):
        if self.has_trained:
            image = Image.open(img)
            faces = self.recognize(image)
            return {"success": True, "faces": faces}
        return {"success": False, "message": "Data is not trained yet."}
