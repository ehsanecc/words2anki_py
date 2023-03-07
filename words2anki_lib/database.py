import sqlite3
from time import time, sleep
from .defaults import *
from uuid import uuid4
from bs4 import BeautifulSoup
from hashlib import sha1
from struct import unpack
from json import dumps

class w2a_db():
    closed = False
    def __init__(self, address:str, deckname:str):
        self.con = sqlite3.connect(address)
        self.con.execute('CREATE TABLE "cards" ( \
            "id"	integer, \
            "nid"	integer NOT NULL, \
            "did"	integer NOT NULL, \
            "ord"	integer NOT NULL, \
            "mod"	integer NOT NULL, \
            "usn"	integer NOT NULL, \
            "type"	integer NOT NULL, \
            "queue"	integer NOT NULL, \
            "due"	integer NOT NULL, \
            "ivl"	integer NOT NULL, \
            "factor"	integer NOT NULL, \
            "reps"	integer NOT NULL, \
            "lapses"	integer NOT NULL, \
            "left"	integer NOT NULL, \
            "odue"	integer NOT NULL, \
            "odid"	integer NOT NULL, \
            "flags"	integer NOT NULL, \
            "data"	text NOT NULL, \
            PRIMARY KEY("id") \
        );')
        self.con.execute('CREATE TABLE "col" (\
            "id"	integer,\
            "crt"	integer NOT NULL,\
            "mod"	integer NOT NULL,\
            "scm"	integer NOT NULL,\
            "ver"	integer NOT NULL,\
            "dty"	integer NOT NULL,\
            "usn"	integer NOT NULL,\
            "ls"	integer NOT NULL,\
            "conf"	text NOT NULL,\
            "models"	text NOT NULL,\
            "decks"	text NOT NULL,\
            "dconf"	text NOT NULL,\
            "tags"	text NOT NULL,\
            PRIMARY KEY("id")\
        );')
        self.con.execute('CREATE TABLE "graves" (\
            "usn"	integer NOT NULL,\
            "oid"	integer NOT NULL,\
            "type"	integer NOT NULL\
        );')
        self.con.execute('CREATE TABLE "notes" (\
            "id"	integer,\
            "guid"	text NOT NULL,\
            "mid"	integer NOT NULL,\
            "mod"	integer NOT NULL,\
            "usn"	integer NOT NULL,\
            "tags"	text NOT NULL,\
            "flds"	text NOT NULL,\
            "sfld"	integer NOT NULL,\
            "csum"	integer NOT NULL,\
            "flags"	integer NOT NULL,\
            "data"	text NOT NULL,\
            PRIMARY KEY("id")\
        );')
        self.con.execute('CREATE TABLE "revlog" (\
            "id"	integer,\
            "cid"	integer NOT NULL,\
            "usn"	integer NOT NULL,\
            "ease"	integer NOT NULL,\
            "ivl"	integer NOT NULL,\
            "lastIvl"	integer NOT NULL,\
            "factor"	integer NOT NULL,\
            "time"	integer NOT NULL,\
            "type"	integer NOT NULL,\
            PRIMARY KEY("id")\
        );')
        self.con.execute('CREATE INDEX "ix_cards_nid" ON "cards" ("nid");')
        self.con.execute('CREATE INDEX "ix_cards_sched" ON "cards" ("did","queue","due");')
        self.con.execute('CREATE INDEX "ix_cards_usn" ON "cards" ("usn");')
        self.con.execute('CREATE INDEX "ix_notes_csum" ON "notes" ("csum");')
        self.con.execute('CREATE INDEX "ix_notes_usn" ON "notes" ("usn");')
        self.con.execute('CREATE INDEX "ix_revlog_cid" ON "revlog" ("cid");')
        self.con.execute('CREATE INDEX "ix_revlog_usn" ON "revlog" ("usn");')

        deck = build_deck(deckname)
        conf = conf_default
        conf['activeDecks'] = [deck['id']]
        conf['curDeck'] = deck['id']
        self.deckId = deck['id']
        self.con.execute('INSERT INTO "col"(crt, mod, scm, ver, dty, usn, ls, conf, models, decks, dconf, tags) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
            [int(time()), int(time()*1000), int(time()*1000), 11, 0, 0, 0, dumps(conf_default), dumps(models_default), dumps(deck['decks']), dumps(deck['dconf']), '{}'])
    
    def insert_card(self, card:dict):
        uid = int(time()*1000)
        self.con.execute('INSERT INTO "cards" (nid, did, ord, mod, usn, type, queue, due, ivl, factor, reps, lapses, left, odue, odid, flags, data) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
            [uid, self.deckId, 0, int(time()), -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '{}'])
        self.con.execute('INSERT INTO "notes" (id, guid, mid, mod, usn, tags, flds, sfld, csum, flags, data) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
            [uid, str(uuid4()), mid_default, int(time()), -1, '', f"{card['headword']}\x1f{card['front']}\x1f{card['back']}", card['front'], 
                unpack('L', sha1(card['front'].encode('utf8')).digest()[:4])[0], 0, ''])
        sleep(0.001) # 
        

    def set_collection(self, mod, conf, models, decks, dconf):
        self.con.execute('UPDATE "col" SET mod=?, conf=?, models=?, decks=?, dconf=? WHERE id=1', [mod, conf, models, decks, dconf])

    def close(self):
        self.con.commit()
        self.con.close()
        self.closed = True

    def __del__(self):
        if not self.closed:
            self.close()