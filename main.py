import os
from http import client
from typing import List, Union
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi import File, UploadFile, FastAPI, Request, status, HTTPException
import boto3
from dotenv import load_dotenv
from exceptions import apiException
import io
from rembg import remove

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




@app.post("/analyze_image_content")
async def upload(file: UploadFile = File()):
    if validate_upload_file(file):
        label_data = client.detect_moderation_labels(Image={'Bytes': await file.read()})
        print(label_data)
        json_compatible_data = jsonable_encoder(label_data)
        return {"status": "false",
                "message": "",
                "data": json_compatible_data['ModerationLabels']
                }


@app.post("/image_backgroud_remover")
async def remove_background2(file: UploadFile = File()):
    validate_upload_file(file)
    img_bytes = await file.read()
    result = remove(img_bytes)
    return StreamingResponse(io.BytesIO(result), media_type="image/png")



@app.exception_handler(apiException)
def api_exception_handler(request: Request, exc: apiException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={'detail': exc.name}
    )

