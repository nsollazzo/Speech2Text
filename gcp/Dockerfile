###########################################
# base image
FROM python:3.8-slim-buster AS base

RUN apt-get update && apt-get upgrade

# installing ffmpeg
RUN apt-get install -y ffmpeg libavcodec-extra

###########################################
# Throwaway image with C compiler installed
FROM base as builder

ADD requirements.txt requirements.txt

RUN pip install wheel

# instead of installing, create a wheel
RUN pip wheel --wheel-dir=/root/wheels -r requirements.txt

###########################################
# Image WITHOUT C compiler but WITH wheels
FROM base

COPY --from=builder /root/wheels /root/wheels
COPY --from=builder /requirements.txt /requirements.txt

# Ignore the Python package index
# and look for archives in
# /root/wheels directory
RUN pip install \
      --no-index \
      --find-links=/root/wheels \
      -r requirements.txt

ADD src /app
ADD api_key.json /api_key.json
WORKDIR /app

CMD ["python", "main.py"]
