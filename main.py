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
from random import shuffle
from words2anki_lib.fetcher import DataFetcher

from words2anki_lib.database import W2ADatabase

argparser = ArgumentParser("Words2Anki Python Edition v1", "Give me a text file with a word in each line, I give you Anki package file :)")
argparser.add_argument("words_file", type=str, help="Text file to read words from")
argparser.add_argument("-o", "--output", type=str, default=None, help="Output filename, default is '<deck name>_<ttstype>'")
# argparser.add_argument("-n", "--name", type=str, help="Dictionary name")
argparser.add_argument("-p", "--pronun", choices=['british', 'american'], default='american', type=str, help="Pornunciation type")
argparser.add_argument("--proxy", type=str, help="Set proxy for http(s) requests")
argparser.add_argument("-d", "--deck", type=str, default=None, help="Set deck name, default=<words_file> name")
argparser.add_argument("-c", "--cache", type=str, default="cache.zip", help="Cache file to use, default=cache.zip")
argparser.add_argument("-t", "--ttstype", type=str, choices=['ankiweb','ankidroid','none'], default='ankidroid', help="Add Text To Speech for back card (meaning)")
argparser.add_argument("--shuffle", action='store_true', help="Shuffle words list")
args = argparser.parse_args()

wordDict = {}
fileList = []
defaultUrl = "https://www.ldoceonline.com/dictionary/"
defaultUserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'

if args.deck == None:
    args.deck = basename(args.words_file).split('.')[0]
if args.output == None:
    args.output = f"{re.sub(r'[^a-zA-Z0-9 ]', '_', args.deck)}_{args.ttstype}.apkg"
elif not re.match(r".*\.apkg$", args.output):
    args.output += ".apkg"
args.pronunciation = {'american':'amefile', 'british':'brefile'}[args.pronun]

def remove_extra_by_selector(e:Tag, selectors:list =['a', '.speaker', 'script', '.ACTIV,.BOX,.COMMENT,.FIELD,.HWD,.NOTE,.Noteprompt,.PICCAL,.PIC,.USAGE']):
    for selector in selectors: # tags or classes
        if selector == 'a':
            for element in e.select(selector): element.replace_with(element.text) # remove link
        else:
            for element in e.select(selector): element.replace_with()
    # remove hidden (display: none)
    for element in e.select('[style*="display: none"]'): element.replace_with()

def expand_refrences(e:BeautifulSoup, fetcher:DataFetcher):
    expanded = False
    baseUrl = fetcher.dictionaries[fetcher.currentDictionary]['baseUrl']
    for cr in e.select("span.Crossref"):
        expanded = True
        href = f"{baseUrl}{cr.select('a.crossRef')[0].get('href')}"
        word = re.match(r".*\/([^\/]+)$", href)
        if word:
            word = word.groups()[0]
            html = fetcher.get(href, word, 'cache')
            if html.ok and html.result:
                html = BeautifulSoup(html.content, 'lxml')
                for sense in html.find_all('span', class_='Sense'):
                    cr.append(BeautifulSoup('<br>', 'lxml').br)
                    for child in sense: cr.append(copy(child))
        cr.unwrap()

    return expanded

def tts_friendly(e:list[Tag]):
    text = []
    for span in e:
        _span = copy(span)
        remove_extra_by_selector(_span, ['script', '.PronCodes'])
        for child in _span.children:
            s = child.text.replace('SYN', 'synonym').replace('OPP', 'opposite')
            s2 = re.sub(r'[^0-9a-zA-Z/\-,\.\\\'’£\$:\(=\)\!\?\n\+\* ]', '', s)
            s3 = re.sub(r"^\n", '', s2)
            s4 = re.sub(r"^ ", "", s3)
            s5 = re.sub(r'\.([a-zA-Z])', '.\n\\1', s4.replace('\n', '.\n'))
            if len(s4.replace('\n', '')):
                text.append(s5)

    return re.sub(r"^ ?\.$", '' , (".\n".join(text).replace('  ', ' ') + ".").replace('..', '.'))

def sort_by_level(words:dict, reverse:bool=True):
    level_word = []
    for word in words:
        if len(words[word]) == 0:
            print("ERROR: empty card!", word, words[word])
            exit()
        level_word.append(f"{words[word][0]['level']}:{word}")
    level_word.sort(reverse=reverse)

    return {k.split(':')[1]:words[k.split(':')[1]] for k in level_word}

def sort_by_words(words:dict):
    words_in_words = {}
    word_relatives = {}
    for word in words:
        words_in_words[word] = []
        for wp in words[word]:
            for w in re.sub('[^a-zA-Z]', '.', wp['ttstext']).split('.'):
                w = w.strip().lower()
                if len(w) > 2 and w not in words_in_words[word] and w != word:
                    words_in_words[word].append(w)

        # calculate relatives
        word_relatives[word] = 0
        for w in words_in_words[word]:
            if w in words.keys():
                word_relatives[word] += 1

    words_relatives_ = [f"{word_relatives[wr]}:{wr}" for wr in word_relatives]
    words_relatives_.sort()

    return {k.split(':')[1]:words[k.split(':')[1]] for k in words_relatives_}

with open(args.words_file, "rt") as wordsFile:
    summary = {'notFound':[], 'error':[], 'fromCache':[], 'skipped':{}}
    fetcher = DataFetcher(args.cache, {'headers':{'User-agent':defaultUserAgent}, 'proxies':{'https':args.proxy}})
    queryNum = 0
    words = wordsFile.read().splitlines()
    if args.shuffle: shuffle(words)
    for word in words:
        word = word.strip()
        if len(word) < 2:
            print(f"Word is too small: {word}")
            continue
        if word in wordDict.keys():
            print(f"Processing {word} ... exists, skip")
            if word in summary['skipped']:
                summary['skipped'][word] += 1
            else:
                summary['skipped'][word] = 1
            continue
        
        print(f"Processing {word} ... getting html", end='\r')
        req = fetcher.get(f"{defaultUrl}{word}", word, 'cache')
        if not req.ok:
            print(f"Processing {word} ... error", end='\r')
            summary['error'].append(word)
            continue
        if not req.result:
            print(f"Processing {word} ... not found, skip")
            summary['notFound'].append(word)
            continue
        html_content = req.content
        if req.fromcache:
            summary['fromCache'].append(word)

        print(f"Processing {word} ... parsing html", end='\r')
        wordDict[word] = []
        bs = BeautifulSoup(html_content, 'lxml')
        entry_content = bs.find("div", class_="entry_content")
        for entry in entry_content.select("span .ldoceEntry.Entry"):
            if expand_refrences(entry, fetcher) and len(entry.find_all("span", class_="Sense")) == 0:
                for PhrVbEntry in entry.find_all("span", class_="PhrVbEntry"):
                    PhrVbEntry.span.span.unwrap()
                    PhrVbEntry.span.unwrap()
                    PhrVbEntry['class'].append('Sense') # expanded Entry!
            if len(entry.find_all("span", class_="Sense")) == 0:
                continue
            word_info = {'headword':word}
            head = copy(entry.find("span", class_="Head"))
            if len(head.select(f".{args.pronunciation}")) > 0:
                mp3_url = head.select(f".{args.pronunciation}")[0]['data-src-mp3']
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

print(f"Sorting {len(wordDict)} words ...")
wordDict = sort_by_words(wordDict)
wordDict = sort_by_level(wordDict)

if len(wordDict) == 0:
    print("No words! exit")
    exit(1)

apkg = ZipFile(args.output, "w", ZIP_BZIP2, compresslevel=9)
# database
db = W2ADatabase(':memory:', args.deck, args.ttstype)
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

print("Summary:"\
    f"\n\tNot Found: {len(summary['notFound'])}"\
    f"\n\tFrom Cache: {len(summary['fromCache'])}"\
    f"\n\tError: {len(summary['error'])}"\
    f"\n\tSkipped: {len(summary['skipped'])}\n")
for category in list(summary.keys()):
    words = list(summary[category].keys()) if type(summary[category]) == dict else summary[category]
    if len(words) > 0 and category != 'fromCache':
        print(f"[{category}]")
        for word in words:
            print(f" {word}")