from pydub import AudioSegment
import wave
import logging
import os

# create logger
log = logging.getLogger('Audio')
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


class Audio(object):

    def __init__(self):
        pass

    def _mp3_to_wav(self, mp3_file_name):
        if mp3_file_name.split('.')[-1] == 'mp3':
            log.info("MP3 to WAV conversion...")
            sound = AudioSegment.from_mp3(mp3_file_name)
            wav_file_name = mp3_file_name.split('.')[0] + '.wav'
            sound.export(wav_file_name, format="wav")
            os.remove(mp3_file_name)
            log.info("...DONE!")
        else:
            log.warning("No MP3's file found")

    def _frame_rate_channel(self, audio_file_name):
        log.info("Checking frame rate and channel...")
        with wave.open(audio_file_name, "rb") as wave_file:
            frame_rate = wave_file.getframerate()
            channels = wave_file.getnchannels()
            log.info("...DONE!")
            return frame_rate, channels

    def _stereo_to_mono(self, audio_file_name):
        log.info("Stereo to mono conversion...")
        sound = AudioSegment.from_wav(audio_file_name)
        sound = sound.set_channels(1)
        sound.export(audio_file_name, format="wav")
        log.info("...DONE!")

    def gcp_normalized_audio(self, audio_file_name):
        log.info("Normalizing audio for Google Cloud Computing...")
        self._mp3_to_wav(audio_file_name)

        # The name of the audio file to transcribe
        frame_rate, channels = self._frame_rate_channel(audio_file_name)

        if channels > 1:
            self._stereo_to_mono(audio_file_name)

        log.info("...DONE!")

        return frame_rate
