#! /usr/bin/env python3

import sqlite3
import os
from collections import Counter
from flask import Flask
from flask import render_template
from flask import redirect


app = Flask(__name__)

db_path = "{}links.db".format(os.getenv("IRC_db_path", "./"))
channel = os.getenv("IRC_channel", "#linkgrabber")
server = os.getenv("IRC_server", "irc.freenode.net")


@app.route("/")
def index():
    return redirect("/1")


@app.route("/<int:page_id>")
def page(page_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    links = []

    limit = str(20)
    offset = str((page_id * 20) - 20)

    for row in c.execute(
        """SELECT * FROM links ORDER BY rowid
                            DESC LIMIT {} OFFSET {}""".format(
            limit, offset
        )
    ):
        links.append(row)

    c.close()

    next_page = page_id + 1
    if page_id - 1 < 1:
        previous_page = 1
    else:
        previous_page = page_id - 1

    return render_template(
        "links.html",
        links=links,
        server=server,
        channel=channel,
        next_page=next_page,
        previous_page=previous_page,
    )


@app.route("/stats")
def stats():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    links = []

    for row in c.execute("""SELECT url FROM links"""):
        links.append(row)

    c.close

    total_links = len(links)

    domains = []

    for url in links:
        url_string = str(url[0])
        host = url_string[: url_string.find("/")]
        if "www" in host:
            host = host[4:]
        domains.append(host)

    return render_template(
        "stats.html",
        hosts=sorted(
            Counter(domains).items(), key=lambda domain: domain[1], reverse=True
        ),
        total=total_links,
        server=server,
        channel=channel,
    )

    # for host, value in Counter(domains).items():
    #    print(host, value)
    # (Counter(domains).values())
