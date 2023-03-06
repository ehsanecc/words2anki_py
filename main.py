import re
from copy import copy
from requests import get
from bs4 import BeautifulSoup
from argparse import ArgumentParser
from os.path import exists, basename
from os import remove
from shutil import copy2
from json import dumps
from zipfile import ZipFile
from glob import glob

from words2anki_lib.database import w2a_db

# TODO:
# 1. read words from text
# 2. fetch one-by-one or multithread from https://www.ldoceonline.com/dictionary/<word>
# 3. using beautifulsoup extract words, (some words will expand to multiple words)
# dictionary defination: <headword> : <word1> => <meanings>
# 4. download mp3 files for words (American only)
# 5. prepare sqlite file

argparser = ArgumentParser("Words2Anki Python Edition v1", "Usage")
argparser.add_argument("words_file", type=str, help="Text file to read words from")
argparser.add_argument("-n", "--name", type=str, help="Dictionary name")
args = argparser.parse_args()

wordDict = {}
fileList = []
defaultUrl = "https://www.ldoceonline.com/dictionary/"
defaultUserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'

def textify(e):
    for element in e.select('a'): element.replace_with(element.text) # remove link
    for element in e.select('.speaker'): element.replace_with() # remove speaker
    for element in e.select('script'): element.replace_with() # remove scripts

with open(args.words_file, "rt") as wordsFile:
    for word in wordsFile.read().splitlines():
        if word in wordDict.keys():
            print(f"Processing {word} ... exists, skip")
            continue
        print(f"Processing {word} ... getting html", end='\r')
        req = get(f"{defaultUrl}{word}", headers={'User-agent':defaultUserAgent})
        if req.ok:
            if re.match(r'.*https:\/\/www\.ldoceonline\.com\/spellcheck\/.*', req.url):
                print(f"Processing {word} ... not found, skip")
                continue
            print(f"Processing {word} ... parsing html", end='\r')
            wordDict[word] = []
            bs = BeautifulSoup(req.text, 'lxml')
            entry_content = bs.find("div", class_="entry_content")
            for entry in entry_content.select("span .ldoceEntry.Entry"):
                word_info = {'headword':word}
                head = copy(entry.find("span", class_="Head"))
                mp3_url = head.select(".amefile")[0]['data-src-mp3']
                filename = re.match(r'.*\/([a-zA-Z0-9-]+\.mp3)\?.*', mp3_url)
                if filename:
                    if exists("media/" + filename.groups()[0]):
                        word_info['mp3'] = filename.groups()[0]
                        fileList.append(word_info['mp3'])
                    else:
                        print(f"Processing {word} ... getting mp3", end='\r')
                        mp3 = get(mp3_url, headers={'User-agent':defaultUserAgent})
                        if mp3.ok:
                            with open(f"media/{filename.groups()[0]}", "wb") as fo:
                                fo.write(mp3.content)
                                word_info['mp3'] = filename.groups()[0]
                                fileList.append(word_info['mp3'])
                textify(head)
                word_info['front'] = '<span class="ldoceEntry Entry">' + "".join([str(i) for i in head]) + '</span>' + \
                    (f"[sound:{word_info['mp3']}]" if 'mp3' in word_info else '')
                head = entry.find("span", class_="Head")
                level = 0 if head.find("span", class_="LEVEL") == None else head.find("span", class_="LEVEL").text.strip().count('●')
                word_info['level'] = level
                if head.find("span", class_="PronCodes") != None:
                    word_info['pronunciation'] = head.find("span", class_="PronCodes").text.strip()
                entry_c = copy(entry)
                textify(entry_c)
                word_info['back'] = '<span class="ldoceEntry Entry">' + "".join(str(sense) for sense in entry_c.find_all("span", class_="Sense")) + '</span>'
                wordDict[word].append(word_info)
                print(f"{len(wordDict):03} Processing {word} ... done" + (" "*10))

    # print(dumps(wordDict, indent=2))

if len(wordDict) == 0:
    print("No words! exit")
    exit(1)

# database
if exists('temp/collection.anki21'):
    remove('temp/collection.anki21')
db = w2a_db("temp/collection.anki21")
for word in wordDict:
    for subword in wordDict[word]:
        db.insert_card(subword)
db.close()

with open("temp/meta", "wb") as fo:
    fo.write(b"\x08\x02")
with open("temp/media", "wt") as fo:
    index = 0
    media = {}
    print(fileList)
    fileList = list(dict.fromkeys(fileList)) # remove duplicates
    print(fileList)
    for file in fileList:
        print(f"copy {file} to {index}")
        copy2(f"media/{file}", f"temp/{index}")
        media[str(index)] = file
        index += 1
    fo.write(dumps(media))
z = ZipFile("output.apkg", "w")
for f in glob("temp/*"):
    z.write(f, arcname=basename(f))
z.close()