#! /usr/bin/env python3

import sqlite3
import os
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index(name=None):
    conn = sqlite3.connect('links.db')
    c = conn.cursor()

    links = []
    channel = os.getenv('IRC_channel', '#linkgrabber')
    server = os.getenv('IRC_server', 'irc.freenode.net')

    for row in c.execute('''SELECT * FROM links '''):
        links.append(row)

    return render_template('links.html',
                            links=links,
                            server=server,
                            channel=channel)

