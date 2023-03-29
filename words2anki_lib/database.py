import sqlite3
from time import time, sleep
from .defaults import *
from uuid import uuid4
from bs4 import BeautifulSoup
from hashlib import sha1
from struct import unpack
from json import dumps
from os.path import dirname, sep

class W2ADatabase():
    closed = False
    module_dir = dirname(__file__)
    def __init__(self, database, deckname:str, ttstype:str):
        self.con = sqlite3.connect(database)
        with open(f"{__file__[0:-3]}.sql", 'rb') as queries:
            for query in queries.read().decode('utf-8').replace('\r', '').split(';\n'):
                self.con.execute(query)

        model = build_model(ttstype)
        self.modelId = list(model.keys())[0]
        deck = build_deck(deckname)
        conf = conf_default
        conf['activeDecks'] = [deck['id']]
        conf['curDeck'] = deck['id']
        self.deckId = deck['id']
        self.con.execute('INSERT INTO "col"(crt, mod, scm, ver, dty, usn, ls, conf, models, decks, dconf, tags) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
            [int(time()), int(time()*1000), int(time()*1000), 11, 0, 0, 0, dumps(conf_default), dumps(model), dumps(deck['decks']), dumps(deck['dconf']), '{}'])
    
    def insert_card(self, card:dict):
        uid = int(time()*1000)
        self.con.execute('INSERT INTO "cards" (id, nid, did, ord, mod, usn, type, queue, due, ivl, factor, reps, lapses, left, odue, odid, flags, data) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
            [uid, uid, self.deckId, 0, int(time()), -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '{}'])
        self.con.execute('INSERT INTO "notes" (id, guid, mid, mod, usn, tags, flds, sfld, csum, flags, data) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
            [uid, str(uuid4()), self.modelId, int(time()), -1, '', f"{card['headword']}\x1f{card['front']}\x1f{card['back']}\x1f{card['ttstext']}", card['front'], 
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