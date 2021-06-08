# FROM alpine:latest
FROM openjdk:8-jre-alpine

RUN apk add --no-cache tesseract-ocr python3 py3-numpy && \
    pip3 install --upgrade pip setuptools wheel && \
    apk add --no-cache --virtual .build-deps gcc g++ zlib-dev make python3-dev py-numpy-dev jpeg-dev && \
    pip3 install matplotlib && \
    apk del .build-deps
RUN apk add python3
RUN apk add cmd:pip3
RUN apk add py-cryptography
RUN apk add bash
RUN apk add py3-sqlalchemy
WORKDIR /app
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python3", "-m", "rest"]
