from google.cloud import storage
from google.oauth2 import service_account
import uuid
# # 서비스 계정 인증 정보가 담긴 JSON 파일 경로
# KEY_PATH = "./config/key.json"
# # Credentials 객체 생성
# credentials = service_account.Credentials.from_service_account_file(KEY_PATH)

bucket_name = 'donut-zpe-bucket-v2'    
image = '/Users/kang/Documents/Github/donut-AI/asset/choco_banana.png'    
stored_name = str(uuid.uuid4())    # 업로드할 파일을 GCP에 저장할 때의 이름

#Image upload to Google Cloud Storage
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(stored_name)

blob.upload_from_filename(image)
print("https://storage.googleapis.com/" + bucket_name + "/" + stored_name)