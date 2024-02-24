import os

from google.cloud import storage
from google.oauth2 import service_account

import uuid
from urllib.parse import urlparse

# # 서비스 계정 인증 정보가 담긴 JSON 파일 경로
KEY_PATH = "adroit-metric-413519-d4e6d7038d34.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=KEY_PATH

bucket_name = 'donut-zpe-bucket-v2'    

# Upload image to Google Cloud Storage
def upload_gcs(enhance_image):
    #Image upload to Google Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(enhance_image)

    blob.upload_from_filename(enhance_image +".jpg")
    return "https://storage.googleapis.com/" + bucket_name + "/" + enhance_image


# Download image to Google Cloud Storage
def download_gcs(DOWNLOAD_DIR, image): 
    parsed = urlparse(image)
    image_name =  parsed.path.split('/')[-1]
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(image_name)

    blob.download_to_filename(DOWNLOAD_DIR+"/"+image_name)
    return DOWNLOAD_DIR+"/"+image_name
