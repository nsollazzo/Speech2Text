import os

from .transcribe import Transcribe

if __name__ == "__main__":
    BUCKET_NAME = "audiofiles"
    FILEPATH = "~/audio_wav/"
    OUTPUT_FILEPATH = "~/Transcripts/"

    transcriber = Transcribe(BUCKET_NAME, FILEPATH, OUTPUT_FILEPATH)

    files = [f for f in os.listdir(FILEPATH) if f.endswith(".wav")]
    for audio_file_name in files:
        exists = os.path.isfile(OUTPUT_FILEPATH + audio_file_name.split('.')[0] + '.txt')
        if exists:
            pass
        else:
            print(audio_file_name)
            transcript = transcriber(audio_file_name)
            transcript_filename = audio_file_name.split('.')[0] + '.txt'
            transcriber.write_transcripts(transcript_filename,transcript)