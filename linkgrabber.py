#! /usr/bin/env python3

import irc.bot
import irc.strings
import datetime
import os
import sqlite3
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from urlextract import URLExtract


class GrabberBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port, db_path):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        if len(a) >1:
            nick = e.source.nick
            extractor = URLExtract()
            urls = extractor.find_urls(a[1].strip())
            with Database(db_path) as db:
                for url in urls:
                    db.execute('INSERT INTO links (datetime, nick, url) VALUES'
                    + ' (?,?,?)', (str(datetime.datetime.now()), nick, url))

                    print('{} {} posted {}'.format(str(datetime.datetime.now()), nick, url))


class Database:
    def __init__(self, name):
        self._conn = sqlite3.connect(name)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

def main():
    db_path = '{}links.db'.format(os.getenv('IRC_db_path', './'))

    with Database(db_path) as db:
       db.execute('''CREATE TABLE IF NOT EXISTS links
                    (datetime, nick, url)''')

    channel = os.getenv('IRC_channel', '#linkgrabber')
    nickname = os.getenv('IRC_nickname', 'grabberbot')
    server = os.getenv('IRC_server', 'irc.freenode.net')
    port = os.getenv('IRC_port', 6667)

    bot = GrabberBot(channel, nickname, server, port, db_path)
    bot.start()



if __name__ == "__main__":
    main()



