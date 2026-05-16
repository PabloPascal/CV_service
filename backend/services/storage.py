from minio import Minio
from minio.error import S3Error
import os 
from typing import Optional
import asyncio
from datetime import timedelta



class Storage:

    def __init__(self):
        self.client = Minio(
            endpoint=os.getenv("MINIO_ENDPOINT", "minio:9000"),
            access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
            secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
            secure=False
        )
        self.bucket_input = os.getenv("BUCKET_INPUT", "input-videos")
        self.bucket_output = os.getenv("BUCKET_OUTPUT", "output-videos")        
        self.ensure()

    def ensure(self):
        for bucket in [self.bucket_input, self.bucket_output]:
            if not self.client.bucket_exists(bucket):
                self.client.make_bucket(bucket)
                print(f"bucket {bucket} created")

    async def upload_file(self, bucket : str, object_name : str, filepath : str)->str:
        """asynchronic uploading file"""
        return await asyncio.to_thread(
            self.sync_upload_file, bucket, object_name, filepath 
        )
        
    def sync_upload_file(self, bucket : str, object_name : str, filepath : str)->str:
        self.client.fput_object(bucket, object_name, filepath)  
        return object_name


    async def upload_object(self, bucket : str, object_name : str, data, length : int)->str:
        return await \
            asyncio.to_thread(self.upload_object_sync, bucket, object_name, data, length)


    def upload_object_sync(self, bucket : str, object_name : str, data, length : int)->str:
        self.client.put_object(bucket, object_name, data, length)
        return object_name
    

    async def download_file(self, bucket : str, object_name : str, file_to_download : str):
        await asyncio.to_thread(
            self.download_file_sync, bucket, object_name, file_to_download
        )


    def download_file_sync(self, bucket : str, object_name : str, file_to_download : str):
        """"method download file to local disk"""
        self.client.fget_object(
            bucket_name=bucket, object_name=object_name, file_path=file_to_download
            )


    def get_presignet_url(self, bucket_name : str, object_name : str, expires : int = 3600)->str:
        return self.client.presigned_get_object(
            bucket_name=bucket_name, 
            object_name=object_name,
            expires=timedelta(seconds=expires)
            )


    async def delete_file(self, bucket_name : str, object_name : str):
        await asyncio.to_thread(self.delete_file_sync, bucket_name, object_name)


    def delete_file_sync(self, bucket_name : str, object_name : str):
        self.client.remove_object(
            bucket_name=bucket_name,
            object_name=object_name
            )


storage_service = Storage()


