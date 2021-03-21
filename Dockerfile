FROM alpine:3.8
RUN apk add python3
RUN apk add py-cryptography
RUN apk add bash
RUN apk add py3-sqlalchemy
WORKDIR /app
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python3", "-m", "rest"]
