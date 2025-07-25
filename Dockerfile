FROM python:3.12-alpine

RUN mkdir -p /usr/src/app/LinkGrabber

COPY LICENSE README.md linkgrabber.py requirements.txt /usr/src/app/LinkGrabber

WORKDIR /usr/src/app/LinkGrabber

RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/cache/apk/*

CMD [ "python", "./linkgrabber.py" ]
