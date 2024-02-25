import os 
import uvicorn
import shutil
import datetime

from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from img_enhancement import i_enhance
from upload_img_gcs import download_gcs, upload_gcs

app = FastAPI()
DOWNLOAD_DIR = './donut-zpe-bucket-v2'


class image_info(BaseModel):
    giftId: int = Form()
    image: UploadFile = File(...)



@app.get("/")
async def test():
    return {"message": "Hello World"}


# 모든 이미지 
@app.post("/api/server/enhancement")
async def enhancement(image: UploadFile = File(...)):
    print("Get Image, time : " +  datetime.datetime.now())

    UPLOAD_DIR = './output'

    if image != None:
        os.makedirs(UPLOAD_DIR, exist_ok=True)  # 디렉토리 생성
        local_path = os.path.normpath(os.path.join(UPLOAD_DIR, image.filename))
        print("local_path")
        print(local_path)
        with open(local_path, 'wb') as buffer:
            shutil.copyfileobj(image.file, buffer)

    # 이미지 강화
    enhanced_path = i_enhance(local_path)
    print("Successfully enhance image, time: "+ datetime.datetime.now())

    # 강화한 이미지 업로드
    imgUrl = upload_gcs(enhanced_path)
    print("Successfully upload image, time: "+ datetime.datetime.now())
    
    return {"resultUrl": imgUrl}



# 버킷에서 다운로드 받고 강화
@app.post("/api/server/bucket/enhancement")
async def enhancement_bucket(request: image_info):
    # 이미지 다운로드
    print("다운로드 진입")
    local_path = download_gcs(DOWNLOAD_DIR, request.image)
    print("Successfully download image")
    print(local_path)

    # 이미지 강화
    enhanced_path = i_enhance(local_path)
    print("Successfully enhance image")

    # 강화한 이미지 업로드
    imgUrl = upload_gcs(enhanced_path)
    print("Successfully upload image")
    
    return {"giftId":request.giftId, "imageUrl" : imgUrl}



# 선택된 것만 강화
@app.post("/api/server/enhancement/optional")
async def enhancement_optional(giftId: int = Form(), image: UploadFile = File(...)):
    print("Get Image, time : " +  str(datetime.datetime.now()))

    UPLOAD_DIR = './output'
    if image != None:
        os.makedirs(UPLOAD_DIR, exist_ok=True)  # 디렉토리 생성
        local_path = os.path.normpath(os.path.join(UPLOAD_DIR, image.filename))
        print("local_path")
        print(local_path)
        with open(local_path, 'wb') as buffer:
            shutil.copyfileobj(image.file, buffer)
    print("Successfully download image, time : " +  str(datetime.datetime.now()))

    # 이미지 강화
    enhanced_path = i_enhance(local_path)
    print("Successfully enhance image, time : " + str(datetime.datetime.now()))

    # 강화한 이미지 업로드
    imgUrl = upload_gcs(enhanced_path)
    print("Successfully upload image, time : " + str(datetime.datetime.now()))
    
    return {"giftId":giftId, "imageUrl" : imgUrl}




if __name__ == '__main__':
    app_str = 'app:app'
    uvicorn.run(app_str, host='34.47.72.193', port=8000, reload=True, workers=1)