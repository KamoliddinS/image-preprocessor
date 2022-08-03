import os
from http import client
from typing import List, Union
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile, FastAPI, Request, status, HTTPException
from livenessmodel import get_liveness_model, get_liveness_model_soft_max
import boto3
from dotenv import load_dotenv
import face_recognition
from exceptions import apiException

## custome componets

from components import read_image_file, encode_face_from_image_bytes, predict_image_class , compare_face_deep_face, face_analyze, predict_liveness

# from tensorflow.keras.preprocessing import image
# model = keras.models.load_model('models/modelAntiSpoofing128x128.h5')
load_dotenv()




client = boto3.client('rekognition', region_name=os.environ['REGION'],
                      aws_access_key_id=os.environ['ACCESSKEYID'],
                      aws_secret_access_key=os.environ['SECRETACCESSKEY'])
app = FastAPI()


def validate_upload_file(file):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="bad media type")
    return True


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/upload_to_compare_with_DeepFace")
async def upload(reference_image: UploadFile = File(), target_image: UploadFile=File()):


    image_ref = read_image_file(await reference_image.read())
    image_target = read_image_file(await target_image.read())

    return {"status": "false",
            "message": "",
            "data": compare_face_deep_face(image_ref, image_target)
            }


@app.post("/upload_to_analyze_face")
async  def upload(file: UploadFile = File()):
    return {"status": "false",
            "message": "",
            "data": face_analyze(read_image_file(await file.read()))
            }


@app.post("/upload")
async def upload(file: UploadFile = File()):
    if validate_upload_file(file):
        label_data = client.detect_moderation_labels(Image={'Bytes': await file.read()})
        print(label_data)
        json_compatible_data = jsonable_encoder(label_data)
        return {"status": "false",
                "message": "",
                "data": json_compatible_data['ModerationLabels']
                }


@app.post("/predict_liveness")
async def upload(file: UploadFile = File()):
    return {"status": "false",
            "message": "",
            "data": str(predict_liveness(read_image_file(await file.read()))[0])
            }

@app.post("/upload_faces_to_compare")
async def uploadFaces(reference: UploadFile = File(), targets: List[UploadFile] = File()):
    validate_upload_file(reference)
    for file in targets:
        validate_upload_file(file)
    reference_img_bytes = await reference.read()
    encoded_reference_face = [encode_face_from_image_bytes(reference_img_bytes)]
    file_names = []
    encoded_targets = []
    to_return = []
    for file in targets:
        file_names.append(file.filename)
        file_img_bytes = await file.read()
        encoded_target = encode_face_from_image_bytes(file_img_bytes)
        encoded_targets.append(encoded_target)
    for face_encoding, file_name in zip(encoded_targets, file_names):
        result = face_recognition.compare_faces(encoded_reference_face, face_encoding)
        to_return.append({'filename': file_name, 'resultFaceComparison': str(result), })
    return {"status": "false",
            "message": "",
            "data": str(to_return)}


def api_exception_handler(request: Request, exc: apiException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={'detail': exc.name}
    )
