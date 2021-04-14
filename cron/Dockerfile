FROM ubuntu:latest
 
WORKDIR /cron
COPY ./ ./
 
RUN apt-get update \
  && apt-get -y install cron \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 --no-cache-dir install --upgrade pip \
  && rm -rf /var/lib/apt/lists/* \
  && pip3 install requests 
 
RUN touch /cron/cron.log

RUN chmod 0600 cronjob
 
RUN crontab -u root cronjob
 
ENTRYPOINT ["cron", "-f"]