from fastapi import FastAPI, File, UploadFile
from boto3.session import Session
import os.path
import uvicorn

#not for deploy
ACCESS_KEY = 'AKIA3ANKXNY72RZ6OOPX'
SECRET_KEY = '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'
BUCKET_NAME = 'star-bucket-demo'

app = FastAPI()
session = Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)


@app.get('/')
def read_list():
    s3 = session.resource('s3')
    my_bucket = s3.Bucket(BUCKET_NAME)
    return [s.key for s in my_bucket.objects.all()]


@app.get('/items/{item_id}')
def read_item(item_id: int, q: str = None):
    return {'item_id': item_id, 'q': q}


@app.get('/download/{item_index}')
def download_file(item_index):
    s3 = session.resource('s3')
    my_bucket = s3.Bucket(BUCKET_NAME)
    my_bucket.download_file(f'{item_index}', f'./static/{item_index}')
    return 'download success'

@app.post('/upload')
def upload_file(file: UploadFile = File(...)):
    upload_key = file.filename
    s3 = session.resource('s3')
    my_bucket = s3.Bucket(BUCKET_NAME)
    my_bucket.put_object(Key=upload_key, Body=file.file)
    return 'upload success'