
# import base64
# from distutils.command.config import config
# import os 
# from http import client
# from http.client import HTTPException

# from telnetlib import STATUS
# from typing import List, Union
# from urllib import response
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse
# import uvicorn
# from fastapi import File, UploadFile, FastAPI
# from uuid import uuid4, UUID
# # from models import Gender, Role, User #this is for latter use 
# import boto3
# from botocore.config import Config

# from dotenv import load_dotenv

# load_dotenv()

# # my_config = Config(
# #     region_name = os.environ['REGION'],
# #     aws_access_key_id =os.environ['ACCESSKEYID'],
# #     aws_secret_access_key=os.environ['SECRETACCESSKEY']
# #     )


# #### initializing and loading env variables ####
# client = boto3.client('rekognition', region_name = os.environ['REGION'],
#     aws_access_key_id =os.environ['ACCESSKEYID'],
#     aws_secret_access_key=os.environ['SECRETACCESSKEY'])
# app = FastAPI()



# @app.get("/")
# def read_root():
#     return {"Hello": "World or Ola"}


# @app.post("/upload")
# def upload(file: bytes = File()):
#     ### TO WRITE FILE SYNC ###
#     # try:
#     #     contents = await file.read()
#     #     with open(file.filename, 'wb') as f:
#     #         f.write(contents)
#     # except Exception:
#     #     return {"message": "There was an error uploading the file"}
#     # finally:
#     #     await file.close()
#     ###                     ###
#     #TODO this should be adopted to moderator answer
 
#     try:
#         filename = file.filename
#         extension =filename.split(".")[1]
#         print(extension)
#     except:
#         print("Ane exception occured")
    
    
#     response =  client.detect_moderation_labels(Image={'Bytes': file})
#     json_compatible_data = jsonable_encoder(response)
#     return JSONResponse(json_compatible_data)
#     # print(response)
#     # for label in response['ModerationLabels']:
            
#     #         # print (label['Name'] + ' : ' + str(label['Confidence']))
#     #         # print (label['ParentName'])
#     #         # return len(response['ModerationLabels'])
#     #         return {"message": f"{label}"}

#     # return {"message": f"No restricted is found  {response}"}


# @app.post("/upload_multi")
# async def upload_multi(files: List[UploadFile] = File(...)):
#     ### TO WRITE FILES IN SYNC ###
#     # for file in files:
#     #     try:
#     #         contents = await file.read()
#     #         with open(file.filename, 'wb') as f:
#     #             f.write(contents)
#     #     except Exception:
#     #         return {"message": "There was an error uploading the file(s)"}
#     #     finally:
#     #         await file.close()
#      ###                     ###

#      #TODO this should be adopted to moderator answer 

#     return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}

# # if __name__ == '__main__':
# #     uvicorn.run(app, port=8000)

