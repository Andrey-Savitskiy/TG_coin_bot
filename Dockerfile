FROM python:3.7.9-slim-stretch

RUN mkdir "/opt"

COPY ./ /opt/bot/
COPY bot.service /etc/systemd/system/

RUN python3 -m pip install -r /opt/bot/requirements.txt

RUN apt-get install systemd
RUN systemctl daemon-reload
RUN systemctl enable bot
RUN systemctl start bot
RUN systemctl status bot
