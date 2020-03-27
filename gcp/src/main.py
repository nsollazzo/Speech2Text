import os
import logging
from moviepy.editor import VideoFileClip

from gcp import GCP

# create logger
log = logging.getLogger('Main')
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


if __name__ == "__main__":
    BUCKET_NAME = "audiolessons"
    VIDEO_FILEPATH_TO_CONVERT = "/media/video/to_convert/"
    VIDEO_FILEPATH_CONVERTED = "/media/video/converted/"
    AUDIO_FILEPATH = "/media/audio/"
    OUTPUT_FILEPATH = "/media/transcripts/"

    gcp = GCP(BUCKET_NAME, AUDIO_FILEPATH, OUTPUT_FILEPATH)

    if os.listdir(VIDEO_FILEPATH_TO_CONVERT):
        log.info("{} Video files found. Starting conversion...".format(
            len(os.listdir(VIDEO_FILEPATH_TO_CONVERT))))

        for video_file_name in os.listdir(VIDEO_FILEPATH_TO_CONVERT):
            video = VideoFileClip(VIDEO_FILEPATH_TO_CONVERT+video_file_name)
            audio = video.audio
            audio_destination = AUDIO_FILEPATH + \
                video_file_name.split('.')[0]+'.mp3'
            audio.write_audiofile(audio_destination)
            os.rename(VIDEO_FILEPATH_TO_CONVERT+video_file_name,
                      VIDEO_FILEPATH_CONVERTED+video_file_name)

        log.info("...DONE!")
    else:
        log.info("No video file found")

    log.info("Beginning Transcription...")

    for audio_file_name in os.listdir(AUDIO_FILEPATH):
        transcript = gcp.google_transcribe(audio_file_name)
        transcript_filename = audio_file_name.split('.')[0] + '.txt'
        gcp.write_transcripts(transcript_filename, transcript)

    log.info("...DONE!")
