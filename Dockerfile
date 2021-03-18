FROM alpine:3.8
RUN apk add python3
RUN apk add py-cryptography
RUN apk add bash
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
CMD ["python3", "-m", "rest"]
