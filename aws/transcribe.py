import json
import time

from .aws import AWS


class Transcribe(object):
    def __init__(self, bucket_name, filepath, output_filepath):
        self.output_filepath = output_filepath
        aws = AWS(filepath, bucket_name)

    def transcribe(self, audio_file_name):

        transcripts = ''

        self.aws.upload_file_to_s3(audio_file_name)

        transcribe = self.aws.boto3.client(
            'transcribe', region_name='us-east-2')
        job_name = audio_file_name.split('.')[0]
        job_uri = "https://s3.us-east-2.amazonaws.com/" + \
            self.aws.bucket_name + "/" + audio_file_name
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': job_uri},
            MediaFormat='wav',
            LanguageCode='en-US',
            OutputBucket_nameName=self.aws.bucket_name
        )
        while True:
            status = transcribe.get_transcription_job(
                TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            time.sleep(5)

        self.aws.download_file_from_s3(audio_file_name)

        transcribe.delete_transcription_job(TranscriptionJobName=job_name)

        self.aws.delete_file_from_s3(audio_file_name)

        with open(audio_file_name.split('.')[0] + '.json') as f:
            text = json.load(f)

        for i in text['results']['transcripts']:
            transcripts += i['transcript']

        os.remove(audio_file_name.split('.')[0] + '.json')

        return transcripts

    def write_transcripts(self, transcript_filename, transcript):
        f = open(self.output_filepath + transcript_filename, "w+")
        f.write(transcript)
        f.close()

