FROM python:3.10-slim

COPY --from=base /usr/share/python3/app /usr/share/python3/app

COPY requirements.txt /usr/share/python3/app/bot/requirements.txt
WORKDIR /usr/share/python3/app/bot/
RUN /usr/share/python3/app/bin/pip install -r requirements.txt

COPY . /usr/share/python3/app/bot


