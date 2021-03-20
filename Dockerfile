FROM alpine:3.8
RUN apk add python3
RUN apk add py-cryptography
RUN apk add bash
WORKDIR /app
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python3", "-m", "rest"]
