import os 
import uvicorn
import shutil

from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from img_enhancement import i_enhance
from upload_img_gcs import download_gcs, upload_gcs

app = FastAPI()

DOWNLOAD_DIR = './donut-zpe-bucket-v2'

class image_info(BaseModel):
    giftId: int
    image: str


@app.get("/")
async def test():
    i_enhance()
    return {"message": "Hello World"}


# 모든 이미지 
@app.post("/api/server/enhancement")
async def enhancement(file: UploadFile = Form(...)):
    UPLOAD_DIR = './output'

    if file != None:
        os.makedirs(UPLOAD_DIR, exist_ok=True)  # 디렉토리 생성
        local_path = os.path.normpath(os.path.join(UPLOAD_DIR, file.filename))
        print("local_path")
        print(local_path)
        with open(local_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

    # 이미지 강화
    enhanced_path = i_enhance(local_path)
    print("Successfully enhance image")

    # 강화한 이미지 업로드
    imgUrl = upload_gcs(enhanced_path)
    print("Successfully upload image")
    
    return imgUrl



# 선택된 이미지만 
@app.post("/api/home/receiver/enhancement")
async def enhancement_optional(request: image_info):
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



if __name__ == '__main__':
    app_str = 'app:app'
    uvicorn.run(app_str, host='127.0.0.1', port=8000, reload=True, workers=1)