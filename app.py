import os 
import uvicorn
import shutil

from fastapi import FastAPI, UploadFile, File
from img_enhancement import i_enhance

app = FastAPI()

result_path = "./results"



@app.get("/")
async def test():
    i_enhance()
    return {"message": "Hello World"}



@app.post("/api/home/receiver/enhancement")
async def enhancement(giftId:int, file: UploadFile = File(...)):
  
    UPLOAD_DIR = './uploadImage'

    if file != None:
        os.makedirs(UPLOAD_DIR, exist_ok=True)  
        local_path = os.path.normpath(os.path.join(UPLOAD_DIR, file.filename))
        print("local_path")
        print(local_path)
        with open(local_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
    #results = i_enhance(local_path,result_path) 
    i_enhance()
    
    return {"message": "Hello World"}
    
    #return  results 



if __name__ == '__main__':
    app_str = 'app:app'
    uvicorn.run(app_str, host='127.0.0.1', port=8000, reload=True, workers=1)