FROM alpine:3.8
RUN apk add python3
RUN apk add bash
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
RUN python3 -m pytest
CMD ["python3", "-m", "rest"]
