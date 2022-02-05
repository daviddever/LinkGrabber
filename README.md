# LinkGrabber

IRC bot to scrape links from a channel, store in a sqlite database and show in a simple web app.


`linkgrabber.py` runs the irc bot and writes the links to the database, using irc and urlextract modules.

`linkshower.py` is a flask application that runs the site (just basic html and css).


![alt text](https://raw.githubusercontent.com/daviddever/LinkGrabber/master/sampleimage.png "Sample Image")

## Configuration

The following can be set as environmental variables

**IRC_db_path**         location to create and access sqlite database default is `./`

**IRC_channel**         irc channel name, default is `#linkgrabber`

**IRC_nickname**        name of the irc bot, default is `linkgrabber`

**IRC_server**          irc server or network to connect to, default is `irc.libera.chat`

**IRC_port**            irc port to use, default is `6667`

## Setup

The app can be setup manually or run using Docker containers

### Docker

Pass the appropriate environmental variables to the containers and be sure to open allow access

for web traffic to the linkshower container and irc traffic to the linkgrabber container. Both

containers will need access to the sqlite database which can be done using a shared volume.


Both containers are based on Alpine, the linkshower container is built from

[tiangolo/meinheld-gunicorn-flask](https://hub.docker.com/r/tiangolo/meinheld-gunicorn-flask) using Meinheld managed by Gunicorn for running the Flask

application.


```
docker run -d -p 6667:6667 -e "IRC_channel=#linkgrabber" \
                           -e "IRC_nickname=grabberbot" \
                           -e "IRC_server=irc.libera.chat" \
                           -e "IRC_db_path=/db/" \
                           -v /db:/db" \
                           daviddever/linkgrabber:0.2
```

```
docker run -d -p 80:80 -e "IRC_channel=#linkgrabber" \
                       -e "IRC_nickname=grabberbot" \
                       -e "IRC_server=irc.libera.chat" \
                       -e "IRC_db_path=/db/" \
                       -v /db:/db" \
                       daviddever/linkshower:0.2
```

Docker Compose example

```
version: "3.7"

services:

  linkgrabber:
    image: daviddever/linkgrabber:0.2
    container_name: link_grabber
    environment:
      - IRC_channel=#linkgrabber
      - IRC_nickname=grabberbot
      - IRC_server=irc.libera.chat
      - IRC_db_path=/db/
    volumes:
      - /db:/db
    ports:
      - "6667:6667"
    restart: unless-stopped

  linkshower:
    image: daviddever/linkshower:0.2
    container_name: link_shower
    environment:
      - IRC_channel=#linkgrabber
      - IRC_nickname=grabberbot
      - IRC_server=irc.libera.chat
      - IRC_db_path=/db/
    volumes:
      - /db:/db
    ports:
      - "80:80"
    restart: unless-stopped
```

### Manually

Flask has a built in web server but this should not be used outside of testing, setting up which

is beyond the of these instructions, if you just want to run the application I recommend using 

the Docker containers (see above) which runs the app with Meinheld and Gunicorn.


Assuming Ubuntu 20.04

**Install pip**

`sudo apt-get install python3-pip`

**Setup virtualenv**

```
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Set environmental variables** (options can be passed to the app as environmental variables detailed above but

an additional environmental variable needs to be set for Flask)

`export FLASK_APP=linkshower.py`

`export IRC_channel=#linkgrabber`

**Start the application**

`./linkgrabber.py`

`flask run`
