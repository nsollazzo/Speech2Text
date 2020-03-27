import boto3
import botocore

class AWS(object):

    def __init__(self, filepath, bucket_name):
        self.boto3 = boto3
        self.filepath = filepath
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3')

    def upload_file_to_s3(self, audio_file_name):

        Key = self.filepath + audio_file_name
        outPutname = audio_file_name

        self.s3.upload_file(Key, self.bucket_name, outPutname)

    def download_file_from_s3(self, audio_file_name):

        s3 = boto3.resource('s3')

        Key = outPutname = audio_file_name.split('.')[0] + '.json'

        try:
            s3.Bucket_name(self.bucket_name).download_file(Key, outPutname)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

    def delete_file_from_s3(self, audio_file_name):

        s3 = boto3.resource('s3')
        s3.Object(self.bucket_name, audio_file_name).delete()
        s3.Object(self.bucket_name, audio_file_name.split('.')[0] + '.json').delete()
