import re
from copy import copy
from bs4 import BeautifulSoup, Tag
from argparse import ArgumentParser
from os.path import exists, basename, sep
from os import remove
from shutil import copy2
from json import dumps
from zipfile import ZipFile, ZIP_BZIP2
from glob import glob
from time import sleep
from io import BytesIO
from words2anki_lib.fetcher import DataFetcher

from words2anki_lib.database import w2a_db

argparser = ArgumentParser("Words2Anki Python Edition v1", "Give me a text file with a word in each line, I give you Anki package file :)")
argparser.add_argument("words_file", type=str, help="Text file to read words from")
argparser.add_argument("-n", "--name", type=str, help="Dictionary name")
argparser.add_argument("-p", "--proxy", type=str, help="Set proxy for http(s) requests")
argparser.add_argument("-d", "--deck", type=str, default="Default", help="Set deck name")
argparser.add_argument("-c", "--cache", type=str, default="cache.zip", help="Cache file to use")
args = argparser.parse_args()

wordDict = {}
fileList = []
defaultUrl = "https://www.ldoceonline.com/dictionary/"
defaultUserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'

def remove_extra_by_selector(e:Tag, selectors:list =['a', '.speaker', 'script', '.ACTIV,.BOX,.COMMENT,.FIELD,.HWD,.NOTE,.Noteprompt,.PICCAL,.PIC,.USAGE']):
    for selector in selectors: # tags or classes
        if selector == 'a':
            for element in e.select(selector): element.replace_with(element.text) # remove link
        else:
            for element in e.select(selector): element.replace_with()
    # remove hidden (display : none)

def tts_friendly(e:list[Tag]):
    text = []
    for span in e:
        _span = copy(span)
        remove_extra_by_selector(_span, ['script', '.PronCodes'])
        for child in _span.children:
            if len(child.text) > 2:
                s = child.text.replace('SYN', 'synonym')
                s2 = re.sub(r'[^0-9a-zA-Z/\-,\.\\\'’:\(=\)\n ]', '', s)
                s3 = re.sub(r"^\n", '', s2)
                s4 = re.sub(r"^ ", "", s3)
                text.append(s4.replace('\n', '.\n'))

    return "." + ".\n".join(text).replace('  ', ' ').replace('..', '.') + "."

with open(args.words_file, "rt") as wordsFile:
    fetcher = DataFetcher(args.cache, {'headers':{'User-agent':defaultUserAgent}, 'proxies':{'https':args.proxy}})
    queryNum = 0
    for word in wordsFile.read().splitlines():
        word = word.strip()
        if len(word) < 2:
            print(f"Word is too small: {word}")
            continue
        if word in wordDict.keys():
            print(f"Processing {word} ... exists, skip")
            continue
        
        print(f"Processing {word} ... getting html", end='\r')
        req = fetcher.get(f"{defaultUrl}{word}", word, 'cache')
        if not req.ok:
            print(f"Processing {word} ... error", end='\r')
            continue
        if not req.result:
            print(f"Processing {word} ... not found, skip")
            continue
        html_content = req.content

        print(f"Processing {word} ... parsing html", end='\r')
        wordDict[word] = []
        bs = BeautifulSoup(html_content, 'lxml')
        entry_content = bs.find("div", class_="entry_content")
        for entry in entry_content.select("span .ldoceEntry.Entry"):
            word_info = {'headword':word}
            head = copy(entry.find("span", class_="Head"))
            if len(head.select(".amefile")) > 0:
                mp3_url = head.select(".amefile")[0]['data-src-mp3']
                filename = re.match(r'.*\/([a-zA-Z0-9-]+\.mp3)\?.*', mp3_url)
                if filename:
                    mp3 = fetcher.get(mp3_url, filename.groups()[0], 'media')
                    if mp3.ok and mp3.result:
                        word_info['mp3'] = filename.groups()[0]
                        fileList.append(word_info['mp3'])

            remove_extra_by_selector(head)
            word_info['front'] = '<span class="ldoceEntry Entry">' + "".join([str(i) for i in head]) + '</span>' + \
                (f"[sound:{word_info['mp3']}]" if 'mp3' in word_info else '')
            head = entry.find("span", class_="Head")
            level = 0 if head.find("span", class_="LEVEL") == None else head.find("span", class_="LEVEL").text.strip().count('●')
            word_info['level'] = level
            if head.find("span", class_="PronCodes") != None:
                word_info['pronunciation'] = head.find("span", class_="PronCodes").text.strip()
            entry_c = copy(entry)
            remove_extra_by_selector(entry_c)
            word_info['back'] = '<span class="ldoceEntry Entry">' + "\n".join(str(sense) for sense in entry_c.find_all("span", class_="Sense")) + '</span>'
            word_info['ttstext'] = tts_friendly(entry_c.find_all("span", class_="Sense")) # friendly with tts :)
            wordDict[word].append(word_info)
            print(f"{len(wordDict):03} Processing {word} ... done" + ("(cached)" if req.fromcache else "" ) + (" "*10))

if len(wordDict) == 0:
    print("No words! exit")
    exit(1)

apkg = ZipFile(f"{args.deck.replace(':', '_')}.apkg", "w", ZIP_BZIP2, compresslevel=9)
# database
db = w2a_db(':memory:', args.deck)
for word in wordDict:
    for subword in wordDict[word]:
        db.insert_card(subword)
apkg.writestr("collection.anki21", db.con.serialize())
db.close()

apkg.writestr("meta", b'\x08\x02') # meta file (which i donno what is for!!)
index = 0
media = {}
fileList = list(dict.fromkeys(fileList)) # remove duplicates
for file in fileList:
    print(f"copy {file} to {index}")
    apkg.writestr(f"{index}", fetcher.get(None, file, 'media').content)
    media[str(index)] = file
    index += 1
apkg.writestr("media", dumps(media))
apkg.close()