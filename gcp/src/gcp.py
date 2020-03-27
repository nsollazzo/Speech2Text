from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import storage

import logging
import datetime

from audio import Audio

# create logger
log = logging.getLogger('GCP')
log.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create file handler
# fhdlr = logging.FileHandler('logs/simulation_py.log')
# fhdlr.setFormatter(formatter)
# logger.addHandler(hdlr)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
log.addHandler(ch)

class GCP(object):
    def __init__(self, bucket_name, filepath, output_filepath):
        self.bucket_name = bucket_name
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.get_bucket(self.bucket_name)
        self.filepath = filepath
        self.output_filepath = output_filepath
        self.audio = Audio()

    def _upload_blob(self, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        log.info("Uploading file to bucket...")
        try:
            log.debug("connected to bucket")
            blob = self.bucket.blob(destination_blob_name)
            if not blob.exists():
                log.info(f"Uploading {destination_blob_name}")
                start = datetime.datetime.now()
                blob.chunk_size = 1024 * 1024 * 16 # Set 8 MB blob size
                blob.upload_from_filename(source_file_name, "audio/wav")
                end = datetime.datetime.now()
                log.info(f"Uploaded {destination_blob_name} {end-start}")
        except Exception as e:
            log.error("An exception occurred: {}".format(e))
            exit(1)
       
        log.info("...DONE!")


    def _delete_blob(self, blob_name):
        """Deletes a blob from the bucket."""
        log.info("Deleting file from bucket...")
        blob = self.bucket.blob(blob_name)

        blob.delete()
        log.info("...DONE!")


    def google_transcribe(self, audio_file_name):
        log.info("Transcribing file...")
        source_file_path = self.filepath + audio_file_name
        
        frame_rate = self.audio.gcp_normalized_audio(source_file_path)

        self._upload_blob(source_file_path, audio_file_name)

        gcs_uri = "gs://{}/{}".format(self.bucket_name, audio_file_name)
        transcript = ''

        client = speech.SpeechClient()
        audio = types.RecognitionAudio(uri=gcs_uri)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=frame_rate,
            language_code='it-IT')

        # Detects speech in the audio file
        log.info("Detecting speech in audio file...")
        start = datetime.datetime.now()
        operation = client.long_running_recognize(config, audio)
        response = operation.result(timeout=10000)
        end = datetime.datetime.now()
        log.info(f"...DONE! {end-start}")

        for result in response.results:
            transcript += result.alternatives[0].transcript

        self._delete_blob(audio_file_name)
        log.info("...DONE!")
        return transcript


    def write_transcripts(self, transcript_filename, transcript):
        log.info("Writing transcripts...")
        with open(self.output_filepath + transcript_filename, 'w') as f: 
            f.write(transcript) 
        log.info("...DONE!")
