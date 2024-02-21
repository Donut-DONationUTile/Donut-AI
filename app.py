import os 
import uvicorn
import shutil

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from img_enhancement import i_enhance
from upload_img_gcs import download_gcs, upload_gcs

app = FastAPI()

result_path = "./results"

class image_info(BaseModel):
    giftId: int
    image: str


@app.get("/")
async def test():
    i_enhance()
    return {"message": "Hello World"}



@app.post("/api/home/receiver/enhancement")
async def enhancement(request: image_info):
    DOWNLOAD_DIR = './donut-zpe-bucket-v2'
    print("다운로드 진입")
    # 이미지 다운로드
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