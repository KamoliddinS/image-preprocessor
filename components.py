from keras.applications.imagenet_utils import decode_predictions
from PIL import Image
import cv2
import numpy as np
import face_recognition
from io import BytesIO
from imageNetModel import model
from deepface import DeepFace
from livenessmodel import get_liveness_model, get_liveness_model_soft_max, get_liveness_model_MobileNetV2

def read_image_file(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image


def encode_face_from_image_bytes(file) -> np.ndarray:
    nparr = np.fromstring(file, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # GET LOCATION OF THE FACES
    location = face_recognition.face_locations(img_np)

    # RETURNS FACE ENCODING
    encodings = face_recognition.face_encodings(img_np, location)[0]
    return encodings

metrics = ["cosine", "euclidean", "euclidean_l2"]
def compare_face_deep_face(image_ref: Image.Image, image_target: Image.Image):
    return DeepFace.verify(np.array(image_ref), np.array(image_target), enforce_detection=False, distance_metric=metrics[1])

def face_analyze(image:Image.Image):
    return DeepFace.analyze(np.array(image),enforce_detection=False,  actions = ['age', 'gender', 'race', 'emotion'])

def predict_image_class(image: Image.Image):
    image = np.asarray(image.resize((224, 224)))[..., :3]
    image = np.expand_dims(image, 0)
    image = image / 127.5 - 1.0
    result = decode_predictions(model.predict(image), 2)[0]
    response = []
    for i, res in enumerate(result):
        resp = {}
        resp["class"] = res[1]
        resp["confidence"] = f"{res[2] * 100:0.2f} %"
        response.append(resp)
    return response



# model = get_liveness_model()
model = get_liveness_model_MobileNetV2()
# model.load_weights("models/modelAntiSpoofing32x32.h5")
# model.load_weights("models/modelAntiSpoofing128x128.h5")
model.load_weights("models/mobilenetv2-best.hdf5")
def predict_liveness(image: Image.Image):
  image = np.asarray(image.resize((224, 224)))[..., :3]

  image= np.expand_dims(image, 0)
  image = image / 255
  return  model.predict(image)